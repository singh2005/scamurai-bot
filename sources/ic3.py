#!/usr/bin/env python3

"""
ic3.py

Scrapes the IC3.gov RSS feed, extracts article content, and generates a summary.

This script focuses ONLY on scraping and summarization.
Posting and storage are handled by external orchestrator scripts.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import logging

from formatter import gpt_formatter

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
RSS_URL = "https://www.ic3.gov/PSA/RSS"


def fetch_article_text(url):
    """
    Fetches the article text from the IC3 article URL.
    Adjust the parser based on IC3.gov page structure.
    """
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch {url} - Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Adjust based on actual IC3 HTML structure
    # Example placeholder:
    article_div = soup.find("div", {"id": "psaContent"})
    if article_div:
        return article_div.get_text(separator=" ", strip=True)

    # Fallback to full page text
    return soup.get_text(separator=" ", strip=True)


def scrape_ic3():
    """
    Scrapes IC3 RSS feed and yields each article's title, link, published date, and formatted mastodon post.
    """
    logging.info("Fetching IC3 RSS feed...")
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")
        pub_date = entry.get("published")
        guid = entry.get("guid")

        logging.info(f"Scraping article: {title}")

        article_text = fetch_article_text(link)
        if not article_text:
            logging.warning(f"Skipping {link} due to empty content.")
            continue

        # Create a Claim-like object or dict for formatting
        claim = type("Claim", (object,), {})()
        claim.title = title
        claim.url = link
        claim.summary = article_text  # Passing full text as summary for now

        formatted_post = gpt_formatter.format_scam_alert_for_mastodon(claim)

        yield {
            "guid": guid,
            "title": title,
            "link": link,
            "pub_date": pub_date,
            "formatted_post": formatted_post
        }


if __name__ == "__main__":
    # Example usage: print summaries to console
    for item in scrape_ic3():
        print(f"Title: {item['title']}")
        print(f"Published: {item['pub_date']}")
        print(f"Link: {item['link']}")
        print(f"Summary: {item['summary']}")
        print("="*80)
