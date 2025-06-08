from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ItemRequest(BaseModel):
    name: str

def fetch_ebay_prices(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    prices = []
    listings = soup.select(".s-item")

    for item in listings:
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")

        # Skip "Shop on eBay" or sponsored headings
        if title_tag is None or "Shop on eBay" in title_tag.text:
            continue

        try:
            price_text = price_tag.text.strip().replace("$", "").replace(",", "")
            price_value = float(price_text.split(" ")[0])
            prices.append({
                "title": title_tag.text.strip(),
                "price": round(price_value, 2)
            })
        except:
            continue

        if len(prices) >= 5:
            break

    return prices


def calculate_recommended_price(prices: list):
    if not prices:
        return "N/A"
    avg_price = sum(p["price"] for p in prices) / len(prices)
    return round(avg_price, 2)

@app.post("/recommend")
def recommend_price(item: ItemRequest):
    prices = fetch_ebay_prices(item.name)
    recommended = calculate_recommended_price(prices)

    return {
        "product": item.name,
        "recommended_price": recommended,
        "sources": prices
    }
