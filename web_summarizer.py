#imports
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import ollama

#Scrape website
async def scrape_website(url):
    print("➡️ Starting browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("➡️ Opening URL...")
        await page.goto(url, wait_until="domcontentloaded")

        print("➡️ Scrolling...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)

        print("➡️ Getting HTML...")
        html = await page.content()

        await browser.close()
        print("✅ Scraping done")

        return html

#Extract text
def extract_text(html):
    print("➡️ Extracting text...")

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    elements = soup.find_all(["h1", "h2", "h3", "p", "li"])

    text = " ".join([
        el.get_text(strip=True)
        for el in elements
        if len(el.get_text(strip=True)) > 30
    ])

    print(f"✅ Extracted {len(text)} characters")
    return text

#Sumnmarize with phi3 through Ollama
def summarize_with_ollama(text):
    print("➡️ Sending to Ollama...")

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "user", "content": f"Summarize:\n{text[:1500]}"}
        ]
    )

    print("✅ Got response from Ollama")
    return response["message"]["content"]

#Main
async def main():
    print("🚀 Script started")

    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    html = await scrape_website(url)
    text = extract_text(html)

    print("\n📄 Preview:\n", text[:30000])

    summary = summarize_with_ollama(text)

    print("\n📌 SUMMARY:\n", summary)

#Run
if __name__ == "__main__":
    asyncio.run(main())
