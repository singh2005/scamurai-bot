from mastodon import Mastodon
import os

def create_mastodon_client():
    return Mastodon(
        access_token=os.getenv("MASTODON_ACCESS_TOKEN"),
        api_base_url=os.getenv("MASTODON_API_BASE_URL")  # e.g. "https://mastodon.social"
    )

def post_toot(text: str):
    client = create_mastodon_client()
    try:
        response = client.status_post(status=text)
        print(f"✅ Toot posted: {response['url']}")
    except Exception as e:
        print(f"❌ Error posting toot: {e}")
