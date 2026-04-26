import requests
from bs4 import BeautifulSoup
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
import time

class SportsScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
        }

    @abstractmethod
    def scrape_headlines(self):
        pass

    def scrape_article_content(self, url):
        try:
            print(f"Fetching content from: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            # Try to find the main article body
            # Most news sites use <article> or specific classes for content
            content_div = soup.find("article") or soup.find("div", class_="article-body") or soup.find("div", id="article-content")

            if content_div:
                # Get all paragraphs
                paragraphs = content_div.find_all("p")
                text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                return text

            # Fallback: get all paragraphs in the body
            paragraphs = soup.find_all("p")
            text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            return text if text else "Content not found"

        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return f"Error scraping content: {e}"

class MarcaScraper(SportsScraper):
    def scrape_headlines(self):
        print(f"Scraping Marca headlines...")
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = []

            # Refined selector for Marca
            # Marca often uses <a> tags with specific classes or inside <h2>/<h3>
            for link in soup.find_all("a", href=True):
                title = link.get_text(strip=True)

                if title and len(title) > 20 and "/futbol/" in link["href"]:
                    url = link["href"] if link["href"].startswith("http") else self.base_url + link["href"]
                    # Avoid duplicates
                    if not any(a['url'] == url for a in articles):
                        articles.append({
                            "source": "marca",
                            "title": title,
                            "url": url,
                            "timestamp": datetime.now().isoformat()
                        })
            return articles[:20] # Limit for testing
        except Exception as e:
            print(f"Error scraping Marca: {e}")
            return []

class AsScraper(SportsScraper):
    def scrape_headlines(self):
        print(f"Scraping AS headlines...")
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = []

            # Refined selector for AS
            # AS often uses <a> tags within <h3> or specific classes
            for link in soup.find_all("a", href=True):
                title = link.get_text(strip=True)

                if title and len(title) > 20 and ("/futbol/" in link["href"] or "/deportes/" in link["href"]):
                    url = link["href"] if link["href"].startswith("http") else self.base_url + link["href"]
                    if not any(a['url'] == url for a in articles):
                        articles.append({
                            "source": "as",
                            "title": title,
                            "url": url,
                            "timestamp": datetime.now().isoformat()
                        })
            return articles[:20] # Limit for testing
        except Exception as e:
            print(f"Error scraping AS: {e}")
            return []

def main():
    scrapers = {
        "marca": MarcaScraper("https://www.marca.com"),
        "as": AsScraper("https://as.com")
    }

    all_news = []
    for name, scraper in scrapers.items():
        headlines = scraper.scrape_headlines()
        print(f"Found {len(headlines)} headlines for {name}")

        for art in headlines:
            # Scrape full content for each headline
            art["content"] = scraper.scrape_article_content(art["url"])
            all_news.append(art)
            time.sleep(1) # Polite scraping

    df = pd.DataFrame(all_news)
    print(df.head())
    df.to_csv("scraped_news.csv", index=False)
    print(f"Saved {len(all_news)} articles with content to scraped_news.csv")

if __name__ == "__main__":
    main()
