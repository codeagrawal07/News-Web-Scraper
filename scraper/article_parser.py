import json
from bs4 import BeautifulSoup,NavigableString
import re
def get_date_in_json(soup):
    json_ld_scripts = soup.find_all("script", type="application/ld+json")

    for script in json_ld_scripts:
        if not script.string:
            continue

        data = json.loads(script.string)
        if not isinstance(data, dict):
            continue

        # datePublished exists only in NewsArticle
        if data.get("@type") == "NewsArticle":
            return data.get("datePublished")[:10]

    return None

def get_Title(soup):
    
    og = soup.find('meta', {"property": "og:title"})
    if og and og.get("content"):
        return og["content"].split("|")[0]
 
    h1 = soup.find("h1").split("|")[0]
    return h1.text.strip() if h1 else "Not Found"
      
def get_author(id,soup):
    # INDIA TODAY
    if id==1:
        author_divs = soup.find_all("div", class_="authdetaisl")
        if author_divs:
            return author_divs[0].get_text(strip=True)
    
    #ZEE NEWS
    if id==3:
        zee_author = soup.find("span", class_="aaticleauthor_name")
        if zee_author:
            text=zee_author.get_text()
            return text
    
    #HINDUSTAN TIMES
    if id==2:
        small = soup.find("small")
        if small:
            return small.get_text(strip=True)
        
    #MINT NEWS meta name="author" content="Sounak Mukhopadhyay" 
    if id==4:
        mint_author=soup.find("meta",{"name":"author"})
        if mint_author:
            return mint_author.get("content")

    return "Not Found"
 
def get_Date(soup):

    meta_date = soup.find("meta", {"property": "article:published_time"})
    if meta_date:
        date = meta_date.get("content", "")[:10]
    else:
        date=get_date_in_json(soup)
    return date 

def shor_description(soup):
    short_desc = soup.find('meta', {"name": "description"})
    if short_desc:
        return short_desc["content"].strip()
    else:
        return "Not Found"


def get_Context(id,soup):
    if id==0:
        content = []
        for p in soup.find_all('p'):
            
                text=p.get_text()
                if text:
                    content.append(text)

        article_text = "\n".join(content)
        return article_text

    content = []
    if id==1:
        for p in soup.find_all("p"):
            for child in p.contents:

                # stop when 
                if getattr(child, "name", None) == "div" and "end_story" in child.get("class", []):
                    return "\n".join(content)

                # plain text
                if isinstance(child, NavigableString):
                    text = child.strip()
                    if text:
                        content.append(text)
                # anchor / strong text
                elif child.name in ["a", "strong","span"]:
                    text = child.get_text(strip=True)
                    if text:
                        content.append(text)
        return "\n".join(content)
    if id==2:
        article=soup.find_all(["div","p"], class_=["content","blogTitle liveBlogHdg"])
        if article:
            for p in article:
                
                # Case 1: Read More block
                if p.find("strong") and "Read More" in p.get_text():
                    None                 
                # Case 2: Normal paragrap
                if p.find('i'):
                    None
                if p.find('h2') and p.find('a'):
                    text=(p.find('p')).get_text()
                    if text:
                        content.append(text)
                else:
                    text = p.get_text(strip=True)
                    if text:
                        content.append(text)
                        
            return  "\n".join(content)
        else :
            article=soup.find_all(["div","p"],id="fullIntroContent")
            if article:
                for p in article:
                    
                    # Case 1: Read More block
                    if p.find("strong") and "Read More" in p.get_text():
                        None                 
                    # Case 2: Normal paragrap
                    if p.find('i'):
                        None
                    if p.find('h2') and p.find('a'):
                        text=(p.find('p')).get_text()
                        if text:
                            content.append(text)
                    else:
                        text = p.get_text(strip=True)
                        if text:
                            content.append(text)
                            
                return  "\n".join(content)
                    
    if id==3:
        article = soup.find(id="fullArticle")
        s=str(article)
        soup1=BeautifulSoup(s,'html.parser')
        container = soup1.find('div', id='fullArticle')
        cleaned_lines = []
        if container:
        
            for junk in container.find_all(['script', 'iframe', 'div', 'ins'], 
                                        class_=['ads-box-300x250', 'recommended_widget', 'googlePopUp', 'mb-3', 'ads-placeholder-internal']):
                junk.decompose()

            # 3. Get all text with a double newline separator to keep it readable
            # strip=True removes leading/trailing whitespace from each chunk
            lines = container.get_text(separator="\n\n", strip=True).split('\n\n')

            # 4. Filter out the specific lines you mentioned
            for line in lines:
                # Skip the Zee News CTA
                if "Add Zee News as a Preferred Source" in line:
                    continue
                # Skip "Also Read" links
                if line.startswith("Also Read-"):
                    continue
                # Skip Agency credits
                if any(credit in line for credit in ["(with IANS inputs)", "(With ANI inputs)"]):
                    continue
                
                cleaned_lines.append(line)
        else:
            print("Article container not found.")
        return "\n".join(cleaned_lines) 
    if id==4:
        cont=soup.find_all("div",class_="storyParagraph")
        content=[]
        for p in cont:
            text=p.get_text()
            if text.startswith("Also Read"):
                continue 
            content.append(text+"\n")
        return "\n".join(content)
        
    
def get_image(id,soup):
    
    img_list=[]
    try:
        img_main_url = (soup.find("meta", {"property": "og:image"}))['content']
        
        if img_main_url:
            img_url= img_main_url.split("/")[-1].split("?")[0]
            img_tag = soup.find("img", src=lambda x: x and img_url in x)
            if img_tag:
                img_list.append({
                    "imgURL":img_tag.get('src') or"",
                    "imgTitle":img_tag.get('title') or"",
                    "imgAlt":img_tag.get('alt') or"",
                    "imgHeight":img_tag.get('height') or"",
                    "imgWidth":img_tag.get('width') or"",})
    except:
          None            
    if id==1:    
        try:   
            img_all=soup.find_all('div',class_="itgimage")
            
            if img_all:
                for item in img_all:
                    img_list.append({
                        "imgURL":item.img.get('src') or"",
                        "imgTitle":item.img.get('title') or"",
                        "imgAlt":item.img.get('alt') or"",
                        "imgHeight":item.img.get('height') or"",
                        "imgWidth":item.img.get('width') or"",})
            return img_list
        except:
            None
    if id==2:
        try:
            img_all=soup.find_all(class_='artImage')
            if img_all:
                for item in img_all:
                    img_list.append({
                        "imgURL":item.img.get('data-src') or item.img.get('data') or "",
                        "imgTitle":item.img.get('title') or"",
                        "imgAlt":item.img.get('alt') or"" })
            return img_list
        except:
            None
    if id==3:
        try:
            img_all=soup.find_all("div",class_="photoimg_container")
            if img_all:
                for item in img_all:
                    img_list.append({
                        "imgURL":item.img.get('data-src') or item.img.get('data') or "" ,
                        "imgTitle":item.img.get('title') or"",
                        "imgAlt":item.img.get('alt') or"" })
            return img_list
        except:
            None
    if id==4:
        img_all=soup.find("figure")
        img_list=[]

        img_list.append({
                "imgURL":img_all.find("img").get('src') or "" ,
                "imgTitle":img_all.find('img').get('title') or"",
                "imgAlt":img_all.find("img").get('alt') or"" 
                })
        return img_list    
    
def extract_twitter_links(soup):
    import json, re

    script = soup.find("script",type="application/json")
    if not script:
        return []

    data = json.loads(script.string)
    data_str = json.dumps(data)

    links = re.findall(
        r"https?://twitter\.com/[A-Za-z0-9_]+/status/\d+",
        data_str
    )
    
    return list(set(links))                    
                   
def get_social_media_Link(id,soup):
        list_of_links=[]
        if id==1:
            listOfArticles = soup.find_all('article')
            if listOfArticles:
                for article in listOfArticles:
                    fram=article.find(['iframe'])
                    if fram:
                        list_of_links.append({
                            "link":fram.get('src') or"",
                            "source":"other"})
                        
            listofTweet=extract_twitter_links(soup)
            if listofTweet:
                for link in listofTweet:
                        list_of_links.append({
                            "link":link or"",
                            "source":"twitter"})                
            return list_of_links            
        if id==0:               
            listofReddit=soup.find_all("blockquote", class_="reddit-embed-bq")            
            if listofReddit:
                for post in listofReddit:
                    link = post.a.get("href")
                    if link:
                        list_of_links.append({
                            "link":link or"",
                            "source":"reddit"})
                        
            listofinstagram=soup.find_all('blockquote',class_="instagram-media")
            if listofinstagram:
                for post in listofinstagram:
                    link = post.get("data-instgrm-permalink")
                    if link:
                        list_of_links.append({
                            "link":link or"",
                            "source":"instagram"})
           
            listofTweet=extract_twitter_links(soup)
            if listofTweet:
                for link in listofTweet:
                        list_of_links.append({
                            "link":link or"",
                            "source":"twitter"}) 
      

            fb_links = re.findall(
                r'https://www\.facebook\.com/plugins[^"\']+',
                str(soup)
            )

            fb_links = [
                {"link": link, "source": "other"}
                for link in set(fb_links)
            ]
            list_of_links.extend(fb_links)
                     
            return list_of_links 
                
                
                
            

