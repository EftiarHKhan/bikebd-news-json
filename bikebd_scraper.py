import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BASE_URL = "https://www.bikebd.com"
NEWS_URL = f"{BASE_URL}/blog/category/news"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BikeNewsScraper/1.0; +https://github.com/yourusername)"
}


def scrape_bikebd_news():
    response = requests.get(NEWS_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup)

    articles = []
    news_cards = soup.select(".single-blog-post")  # Each news card

    for card in news_cards:
        #print(card)
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

    # Save to JSON file
    with open("bike_news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(articles)} news articles and saved to bike_news.json")


if __name__ == "__main__":
    scrape_bikebd_news()
