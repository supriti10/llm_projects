import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import google.generativeai as genai


# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Step 1: Scrape Website (JS rendered properly)
# -----------------------------
async def scrape_website(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle")

        # Scroll to load dynamic content
        await page.evaluate("""
            window.scrollTo(0, document.body.scrollHeight)
        """)
        await page.wait_for_timeout(2000)

        html = await page.content()
        await browser.close()

        return html


# -----------------------------
# Step 2: Extract meaningful text (IMPROVED)
# -----------------------------
def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove junk elements
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Focus on useful content tags
    elements = soup.find_all(["h1", "h2", "h3", "p", "li"])

    text_list = []
    for el in elements:
        txt = el.get_text(strip=True)

        # Filter out tiny/noisy text
        if len(txt) > 30:
            text_list.append(txt)

    content = " ".join(text_list)

    return content


# -----------------------------
# Step 3: Gemini summarization
# -----------------------------
def summarize_with_gemini(text):
    system_prompt = (
        "You are a helpful assistant that summarizes website content clearly, "
        "in simple language, using bullet points and sections."
    )

    user_prompt = f"""
    Summarize the following website content.

    Focus on:
    - About the person
    - Skills
    - Projects
    - Experience

    Content:
    {text[:4000]}
    """

    prompt = f"{system_prompt}\n\n{user_prompt}"

    response = model.generate_content(prompt)
    return response.text


# -----------------------------
# Step 4: Main pipeline
# -----------------------------
async def main():
    url = "https://portfolio-sm-iota.vercel.app/"

    print("🔍 Scraping website...")
    html = await scrape_website(url)

    print("🧹 Extracting content...")
    clean_text = extract_visible_text(html)

    # DEBUG (optional)
    print("\n--- Extracted Content Preview ---\n")
    print(clean_text[:10000])

    print("\n🤖 Generating summary with Gemini...\n")
    summary = summarize_with_gemini(clean_text)

    print("📌 SUMMARY:\n")
    print(summary)


# Run
if __name__ == "__main__":
    asyncio.run(main())