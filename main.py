from dotenv import load_dotenv
load_dotenv()

from sources import ftc
from formatter import gpt_formatter
from poster import mastodon
from persistence import s3_client
from persistence.s3_persistence import load_posted_claim_ids, save_posted_claim_ids

print("🔧 Fetching scam alerts from FTC...")
claims = ftc.get_latest_claims(limit=1)

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
        print(f"❌ Error processing claim: {e}")

    print("-" * 40)
