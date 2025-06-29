from openai import OpenAI
client = OpenAI()

def format_scam_alert_for_mastodon(claim):
    prompt = f"""
You are Scamurai-bot, a consumer protection assistant.

Summarize the scam alert below into a **single Mastodon post under 500 characters**. It must include:
- Who is targeted
- How the scam works
- How to avoid it
- A short call to action
- The scam alert URL at the end
- Relevant hashtags

✅ Strict rules:
- Do NOT exceed 500 characters including spaces and URL.
- Write concisely using plain language and emojis.
- No markdown formatting. No line breaks if character limit is at risk.
- The URL is: {claim.url}

Here is the scam alert summary:

Title: {claim.title}
Summary: {claim.summary}

Return only the final Mastodon post text, nothing else.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return None
