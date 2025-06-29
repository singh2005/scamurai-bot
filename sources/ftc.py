import requests
import feedparser
from datetime import datetime
from models import Claim

RSS_FEED_URL = "https://consumer.ftc.gov/blog/gd-rss.xml"

def get_latest_claims(limit=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }
    
    response = requests.get(RSS_FEED_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch feed: {response.status_code}")
        return []
    
    feed = feedparser.parse(response.content)
    print(f"Feed bozo (parse errors): {feed.bozo}")
    print(f"Number of entries parsed: {len(feed.entries)}")
    
    entries = feed.entries[:limit]
    claims = []

    for entry in entries:
        title = entry.title
        summary = getattr(entry, 'summary', '')
        url = entry.link
        published = getattr(entry, 'published', None)

        if published:
            try:
                published_date = datetime(*entry.published_parsed[:6])
            except Exception:
                published_date = datetime.now()
        else:
            published_date = datetime.now()

        claim = Claim(
            title=title,
            verdict="Scam Alert",
            summary=summary,
            url=url,
            date=published_date,
            source="FTC"
        )
        claims.append(claim)

    return claims

if __name__ == "__main__":
    claims = get_latest_claims(limit=3)
    for c in claims:
        print(f"🔍 {c.title}")
        print(f"✅ Verdict: {c.verdict}")
        print(f"📝 Summary: {c.summary}")
        print(f"🔗 URL: {c.url}")
        print(f"📅 Date: {c.date}")
        print("-" * 80)
