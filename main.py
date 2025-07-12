from dotenv import load_dotenv
load_dotenv()

from sources import ftc
from sources.ic3 import scrape_ic3
from formatter import gpt_formatter
from poster import mastodon
from persistence import s3_client
from persistence.s3_persistence import load_posted_claim_ids, save_posted_claim_ids

# Load previously posted claim IDs
posted_ids = load_posted_claim_ids()

# ==============================
# 🔧 Fetching scam alerts from FTC
# ==============================
print("🔧 Fetching scam alerts from FTC...")
claims = ftc.get_latest_claims(limit=20)

print(f"📦 Received {len(claims)} scam alerts")

posted_ids = load_posted_claim_ids()

for claim in claims:
    if claim.url in posted_ids:
        print(f"⏭️ Already posted: {claim.url}")
        continue

    print(f"🔍 {claim.title}")

    try:
        post_text = gpt_formatter.format_scam_alert_for_mastodon(claim)
        print(f"📝 Summary Post:\n{post_text}\n")

        mastodon.post_toot(post_text)
        posted_ids.add(claim.url)
        save_posted_claim_ids(posted_ids)

    except Exception as e:
        print(f"❌ Error processing FTC claim: {e}")

    print("-" * 40)

# ==============================
# 🔧 Fetching scam alerts from IC3
# ==============================
print("🔧 Fetching scam alerts from IC3...")
ic3_claims = scrape_ic3()
ic3_claims = list(ic3_claims)
print(f"📦 Received {len(ic3_claims)} scam alerts from IC3")

for item in ic3_claims:
    if item["link"] in posted_ids:
        print(f"⏭️ Already posted: {item['link']}")
        continue

    print(f"🔍 {item['title']}")

    try:
        post_text = item["formatted_post"]
        print(f"📝 Summary Post:\n{post_text}\n")

        mastodon.post_toot(post_text)
        posted_ids.add(item["link"])
        save_posted_claim_ids(posted_ids)

    except Exception as e:
        print(f"❌ Error processing IC3 claim: {e}")

    print("-" * 40)
