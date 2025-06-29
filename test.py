# test.py

import os
from dotenv import load_dotenv
load_dotenv()  # 🔧 Loads .env variables
from sources import ftc
from formatter import gpt_formatter
# from poster import mastodon  # Uncomment if you want to test posting

def test_ftc_scraper():
    print("\n🔧 Testing FTC scraper...")
    claims = ftc.get_latest_claims(limit=1)
    assert len(claims) > 0, "No claims fetched from FTC."
    print(f"✅ FTC scraper fetched {len(claims)} claim(s).")
    return claims[0]

def test_gpt_formatter(claim):
    print("\n🔧 Testing GPT formatter...")
    post_text = gpt_formatter.format_scam_alert_for_mastodon(claim)
    assert post_text is not None and len(post_text) > 0, "GPT formatter returned empty output."
    print(f"✅ GPT formatter output ({len(post_text)} chars):\n{post_text}")
    return post_text

def test_mastodon_post(post_text):
    print("\n🔧 Testing Mastodon posting... (skipped by default)")
    from poster import mastodon
    mastodon.post_toot(post_text)

if __name__ == "__main__":
    print("🚨 Running Scamurai Bot Tests 🚨")
    
    claim = test_ftc_scraper()
    post_text = test_gpt_formatter(claim)
    
    if os.getenv("TEST_POST_TO_MASTODON") == "true":
        test_mastodon_post(post_text)
    
    print("\n✅ All tests completed successfully.")
