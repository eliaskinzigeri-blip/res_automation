import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

def get_pain_points():
    print("🔍 Scanning Reddit via Public Interface (No API Key needed)...")

    # High-value subreddits
    subreddits = ["smallbusiness", "saas", "homeautomation", "productivity", "solopreneur"]
    # Using a slightly different search strategy for public pages
    # We look for 'top' or 'hot' threads with keywords in title
    pain_keywords = ["how do i", "why is it so hard", "alternative to", "struggling with", "waste of time"]

    found_threads = []

    for sub_name in subreddits:
        print(f"Scanning r/{sub_name}...")
        # Reddit's public JSON interface: add .json to any URL
        url = f"https://www.reddit.com/r/{sub_name}/hot.json?limit=25"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari valet/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])

                for post in posts:
                    post_data = post['data']
                    title = post_data['title'].lower()
                    if any(kw in title for kw in pain_keywords):
                        found_threads.append({
                            "title": post_data['title'],
                            "url": f"https://www.reddit.com{post_data['permalink']}",
                            "text": post_data['selftext'],
                            "subreddit": sub_name
                        })
            else:
                print(f"⚠️ Could not access r/{sub_name}, status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error scanning r/{sub_name}: {str(e)}")

    return found_threads

def analyze_with_groq(thread):
    print(f"🧠 Analyzing thread: {thread['title'][:50]}...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    Analyze this Reddit thread from r/{thread['subreddit']}.
    Title: {thread['title']}
    Content: {thread['text']}

    Extract the EXACT technical or business pain point.
    Ignore generic complaints.
    Return ONLY a JSON object:
    {{
        "pain_point": "clear description of the problem",
        "target_audience": "who has this problem",
        "intent": "what are they trying to achieve"
    }}
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    threads = get_pain_points()
    if threads:
        # Pick a random thread from the found ones to avoid always doing the first one
        import random
        target = random.choice(threads)
        best_pain = analyze_with_groq(target)
        print(f"✅ Found Pain Point: {best_pain}")
        with open("current_pain.json", "w") as f:
            f.write(best_pain)
    else:
        print("❌ No pain points found today.")
