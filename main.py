from dotenv import load_dotenv
load_dotenv()

from sources import ftc
from formatter import gpt_formatter
from poster import mastodon  # your Mastodon poster module

print("🔧 Fetching scam alerts from FTC...")
claims = ftc.get_latest_claims(limit=3)
print(f"📦 Received {len(claims)} scam alerts")

for claim in claims:
    print(f"🔍 {claim.title}")
    post_text = gpt_formatter.format_scam_alert_for_mastodon(claim)
    print(f"📝 Summary Post:\n{post_text}\n")

    # Post to Mastodon
    mastodon.post_toot(post_text)
