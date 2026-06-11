import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def generate_expert_content():
    if not os.path.exists("current_pain.json"):
        print("❌ No pain point found. Run sentinelle.py first.")
        return

    with open("current_pain.json", "r") as f:
        pain_data = json.load(f)

    print(f"✍️ Synthesizing expert content for: {pain_data['pain_point']}...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Phase 1: Strategic Synthesis (Simulating Research)
    research_prompt = f"""
    The user is struggling with: {pain_data['pain_point']}.
    They are: {pain_data['target_audience']}.
    Their goal is: {pain_data['intent']}.

    Act as a senior consultant. Research the most common failure points for this specific problem.
    Identify 3 reasons why standard AI-generated advice fails for this problem.
    Identify 2 'insider' tips that only someone with 10 years of experience would know.

    Format the output as a technical brief.
    """

    research_result = client.chat.completions.create(
        messages=[{"role": "user", "content": research_prompt}],
        model="llama-3.1-70b-versatile"
    ).choices[0].message.content

    # Phase 2: Anti-AI Drafting
    draft_prompt = f"""
    Use the following research to write a high-authority guide:
    ---
    {research_result}
    ---

    STRICT CONSTRAINTS:
    1. NO "AI-isms": Do NOT use words like 'Revolutionary', 'In today's digital landscape', 'Essential', 'Let's dive in'.
    2. TONE: Dry, analytical, evidence-based. Use a "No-BS" tone.
    3. STRUCTURE:
       - [The Hard Truth]: Why this problem is actually difficult.
       - [The Standard Fail]: Why most tutorials online are wrong.
       - [The Proven Path]: Step-by-step solution using real-world logic.
       - [The Verdict]: Final summary of the most efficient setup.
    4. FORMAT: Use Markdown. Use bold text for key warnings. Use tables for comparisons.

    Write the full article in French.
    """

    final_article = client.chat.completions.create(
        messages=[{"role": "user", "content": draft_prompt}],
        model="llama-3.1-70b-versatile"
    ).choices[0].message.content

    with open("final_article.md", "w", encoding="utf-8") as f:
        f.write(final_article)

    print("✅ Article generated: final_article.md")

if __name__ == "__main__":
    generate_expert_content()
