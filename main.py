import os
import subprocess
from datetime import datetime

def run_script(name):
    print(f"🚀 Running {name}...")
    result = subprocess.run(["python", f"{name}.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error in {name}: {result.stderr}")
        return False
    return True

def main():
    print("🛠️ Starting RES Automation Cycle...")

    # 1. Sourcing
    if not run_script("sentinelle"): return

    # 2. Synthesis
    if not run_script("synthetiseur"): return

    # 3. Distribution
    if not run_script("multiplicateur"): return

    # 4. Archiving for the Website
    if os.path.exists("final_article.md"):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"guide_{date_str}.md"

        # Ensure the Astro content folder exists
        os.makedirs("website/src/content/guides", exist_ok=True)

        with open("final_article.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Add Frontmatter for Astro
        frontmatter = f"---\ntitle: \"Guide du {date_str}\"\ndate: {date_str}\n---\n\n"

        with open(f"website/src/content/guides/{filename}", "w", encoding="utf-8") as f:
            f.write(frontmatter + content)

        print(f"✅ Article archived to website: {filename}")

    print("✨ Cycle Complete. System is waiting for the next trigger.")

if __name__ == "__main__":
    main()
