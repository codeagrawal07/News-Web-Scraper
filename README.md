# 📰 News Web Scraper with GUI (India Today, Zee News, Hindustan Times)

A robust Python-based **news scraping application** that automatically extracts **title, author, date, full content, images, and embedded social media posts** from multiple Indian news websites.  
The project also includes a **GUI built with Streamlit** for interactive usage.

---

## 🚀 Features

✅ Scrapes news articles from:
- India Today
- Zee News
- Hindustan Times

✅ Extracts the following data:
- Article Title
- Author Name
- Published Date
- Short Description
- Full Article Content
- All related images
- Embedded social media content (Instagram, Facebook, X/Twitter, videos via iframe)

✅ Handles:
- Multiple HTML layouts
- JSON-LD metadata
- iframe-based social media embeds
- Fallback logic for different websites
- reduce bot detection

✅ Interactive GUI:
- Enter article URL
- View extracted data in a clean dashboard
- Image previews
- Embedded social media posts/videos rendered directly in the UI

---

## 🛠 Tech Stack

- **Python**
- **BeautifulSoup (bs4)** – HTML parsing
- **Requests** – HTTP requests
- **Streamlit** – GUI / Web interface
- **JSON-LD parsing**
- **HTML5 iframe handling**

---

## 🧠 How It Works

1. User enters a **news article URL** in the GUI.
2. The scraper fetches the HTML using `requests`.
3. `BeautifulSoup` parses the DOM.
4. Data is extracted using:
   - Semantic HTML tags
   - JSON-LD metadata
   - Site-specific fallback selectors
5. Images are rendered using `st.image()`.
6. Social media embeds (Instagram, Facebook, X, YouTube) are extracted from `<iframe>` tags and displayed using Streamlit iframe components.

---

## 🖥 GUI Preview

- Expandable article view
- Clean layout for content
- Inline images
- Embedded social media posts/videos

