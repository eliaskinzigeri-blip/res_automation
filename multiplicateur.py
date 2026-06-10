import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def distribute_content():
    if not os.path.exists("final_article.md"):
        print("❌ No article found. Run synthetiseur.py first.")
        return

    with open("final_article.md", "r", encoding="utf-8") as f:
        article = f.read()

    print("📢 Generating distribution assets...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    distribution_prompt = f"""
    Based on this high-authority article, generate:
    1. A LinkedIn post that starts with a controversial hook about the problem and provides a 3-bullet point summary.
    2. A X (Twitter) thread (5 tweets) that simplifies the solution.
    3. A meta-description (160 chars) for the web page.

    Article content:
    {article}

    Format as JSON:
    {{
        "linkedin": "...",
        "twitter_thread": ["tweet 1", "tweet 2", ...],
        "meta_description": "..."
    }}
    """

    assets = client.chat.completions.create(
        messages=[{"role": "user", "content": distribution_prompt}],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    ).choices[0].message.content

    with open("distribution_assets.json", "w", encoding="utf-8") as f:
        f.write(assets)

    print("✅ Distribution assets generated: distribution_assets.json")

if __name__ == "__main__":
    distribute_content()
