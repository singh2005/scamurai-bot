import feedparser
import logging
from models import Claim

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
RSS_URL = "https://www.ic3.gov/PSA/RSS"


def get_latest_claims(limit=5):
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries[:limit]
    claims = []

    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")
        pub_date = entry.get("published")
        guid = entry.get("guid")

        claim = Claim(
            title=title,
            verdict="Scam Alert",
            summary=title,
            url=link,
            date=pub_date,
            source="IC3"
        )
        claims.append(claim)

    return claims       
