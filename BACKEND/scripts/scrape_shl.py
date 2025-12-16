import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_soup(url):
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def scrape_catalog():
    soup = get_soup(CATALOG_URL)

    assessments = []
    links = set()

    # Collect all product links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/solutions/products/" in href and "job-solutions" not in href:
            links.add(BASE_URL + href)

    print(f"Found potential links: {len(links)}")

    for url in links:
        try:
            detail = get_soup(url)

            h1 = detail.find("h1")
            if not h1:
                continue

            name = h1.text.strip()

            desc = detail.find("div", class_="rich-text")
            description = desc.text.strip() if desc else ""

            assessment = {
                "name": name,
                "url": url,
                "description": description
            }

            assessments.append(assessment)
            time.sleep(0.4)

        except Exception as e:
            print("Skipped:", url)

    print(f"Total assessments scraped: {len(assessments)}")

    with open("../data/assessments.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    scrape_catalog()
