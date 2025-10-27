import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

BASE_URL = "https://www.bikebd.com"
NEWS_URL = f"{BASE_URL}/blog/category/news"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BikeNewsScraper/1.0; +https://github.com/yourusername)"
}


def scrape_page(url):
    """Scrape a single page and return articles."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    news_cards = soup.select(".single-blog-post")  # Each news card

    for card in news_cards:
        title_tag = card.select_one(".blog-post-tittle")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        description = card.select_one(".blog-post-text").get_text(strip=True)
        #link = BASE_URL + title_tag["href"]

        # Get image
        img_tag = card.select_one("img")
        image = img_tag["data-original"] if img_tag else None

        # Get date if available
        date_tag = card.select_one(".bp-user-name")
        date = date_tag.get_text(strip=True) if date_tag else None

        articles.append({
            "title": title,
            "description": description,
            #"url": link,
            "image": image,
            "date": date,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return articles


def scrape_bikebd_news():
    """Scrape all pages of bike news."""
    all_articles = []
    page = 1
    
    print("🚴 Starting to scrape bike news from all pages...")
    
    while True:
        # Construct URL for current page
        if page == 1:
            url = NEWS_URL
        else:
            url = f"{NEWS_URL}?page={page}"
        
        print(f"📄 Scraping page {page}: {url}")
        
        try:
            articles = scrape_page(url)
            
            # If no articles found, we've reached the end
            if not articles:
                print(f"✋ No more articles found on page {page}. Stopping.")
                break
            
            all_articles.extend(articles)
            print(f"   Found {len(articles)} articles (Total: {len(all_articles)})")
            
            # Move to next page
            page += 1
            
            # Be polite to the server - add a small delay between requests
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error scraping page {page}: {e}")
            break

    # Save to JSON file
    with open("bike_news.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraped {len(all_articles)} total news articles from {page-1} pages")
    print(f"💾 Saved to bike_news.json")


if __name__ == "__main__":
    scrape_bikebd_news()
