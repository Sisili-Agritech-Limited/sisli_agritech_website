import asyncio
import os
from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def scrape_site():
    print("Starting Playwright...")
    
    # Create a directory for images
    image_dir = os.path.join("assets", "images")
    os.makedirs(image_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # This function listens to all network responses
        async def handle_response(response):
            # Check if the resource downloaded is an image
            if response.request.resource_type == "image":
                try:
                    url = response.url
                    # Extract the filename from the URL
                    parsed_url = urlparse(url)
                    filename = os.path.basename(parsed_url.path)
                    
                    if not filename:
                        filename = "unnamed_image.png"
                        
                    # Get the raw image bytes
                    body = await response.body()
                    
                    # Save the image locally
                    filepath = os.path.join(image_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(body)
                    print(f"Saved image: {filename}")
                except Exception as e:
                    # Some images might be base64 data URIs or fail to download
                    pass

        # Tell Playwright to run our function on every response
        page.on("response", handle_response)
        
        url = "https://sisili.co.ke"
        print(f"Navigating to {url} and downloading images...")
        
        # Go to the page and wait for loading to finish
        try:
            await page.goto(url, wait_until="load", timeout=60000)
            # Wait a few extra seconds to let any delayed images pop in
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Warning during page load: {e}")
        
        # Extract the fully rendered HTML
        html_content = await page.content()
        
        # Save to a local file
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("Successfully saved the rendered HTML to index.html!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_site())
