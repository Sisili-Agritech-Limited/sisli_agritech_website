import asyncio
from playwright.async_api import async_playwright

async def scrape_site():
    print("Starting Playwright...")
    async with async_playwright() as p:
        # Launch browser (headless by default)
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        url = "https://sisili.co.ke"
        print(f"Navigating to {url}...")
        
        # Go to the page and wait for network activity to settle
        await page.goto(url, wait_until="networkidle")
        
        # Extract the fully rendered HTML
        html_content = await page.content()
        
        # Save to a local file
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("Successfully saved the rendered HTML to index.html!")
        
        await browser.close()

if __name__ == "__main__":
    # Windows-specific fix for asyncio event loop
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(scrape_site())
