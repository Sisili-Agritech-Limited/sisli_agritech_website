import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def clean_html():
    print("Loading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove 3rd party SDKs and tracking scripts that slow down page load
    print("Removing bloat scripts...")
    bad_script_domains = [
        "connect.facebook.net",
        "platform.twitter.com",
        "googletagmanager.com",
        "google-analytics.com",
        "tawk.to",        # common live chat
        "zopim.com",      # common live chat
        "tidio.com"       # common live chat
    ]
    
    for script in soup.find_all("script"):
        src = script.get("src", "")
        # Remove if it contains any bad domain
        if any(domain in src for domain in bad_script_domains):
            script.decompose()
            continue
        
        # Also remove inline scripts for these services
        if script.string and any(domain in script.string for domain in bad_script_domains):
            script.decompose()

    # 2. Update Image Tags to point to our downloaded local images
    print("Relinking images to local folder...")
    image_dir = os.path.join("assets", "images")
    
    # We will get a list of all images we successfully downloaded
    local_images = set(os.listdir(image_dir)) if os.path.exists(image_dir) else set()

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
            
        # Parse the filename from the src URL
        filename = os.path.basename(urlparse(src).path)
        
        if filename in local_images:
            # Change the src to our local path
            img["src"] = f"assets/images/{filename}"
            # Also clean up srcset if it exists (which causes browser to still fetch remote)
            if img.has_attr("srcset"):
                del img["srcset"]

    # 3. Clean up the large inline social CSS block (fuse_social_icons_links) which clutters the head
    # (Optional, but helps with clean code)
    for style in soup.find_all("style"):
        if style.string and ".fuse_social_icons_links" in style.string:
            style.decompose()

    # Write cleaned HTML
    print("Saving to index.html...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    print("Successfully cleaned HTML! Page should now load instantly.")

if __name__ == "__main__":
    clean_html()
