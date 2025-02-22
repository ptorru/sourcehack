from dotenv import load_dotenv
from os import environ

load_dotenv()
FIRECRAWL_API_KEY = environ["FIRECRAWL_API_KEY"]

from firecrawl import FirecrawlApp

# app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # Crawl a website:
# scrape_result = app.scrape_url("firecrawl.dev", params={"formats": ["markdown"]})

# print(scrape_result)


import requests
from bs4 import BeautifulSoup


def get_links_from_url(url):

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    the_links = [a.get("href") for a in soup.find_all("a", href=True)]

    return [link for link in the_links if link.startswith("http")][:3]


print(get_links_from_url("https://firecrawl.dev"))
