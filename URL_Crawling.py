import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

def generate_sitemap(url_list):
    """Takes a list of URLs and generates a sitemap.xml file."""
    print(f"\nWriting {len(url_list)} URLs to sitemap.xml...")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sorted(list(url_list)): 
            f.write('  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')
    print("Sitemap.xml generated successfully!")

def main():
    """Main function to crawl the site and generate the sitemap."""
    base_url = "https://www.finploy.com"

    urls_to_visit = [base_url]
    visited_urls = set()

    print("Setting up Chrome WebDriver...")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    print("WebDriver is ready. Starting crawl")

    try:
        while urls_to_visit:
            current_url = urls_to_visit.pop(0)

            if current_url in visited_urls:
                continue

            print(f"Crawling: {current_url}")
            visited_urls.add(current_url)

            try:
                driver.get(current_url)
                time.sleep(2) 
                page_source = driver.page_source
                
                soup = BeautifulSoup(page_source, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link['href']
                   
                    absolute_url = urljoin(base_url, href)

                    if not absolute_url.startswith(base_url):
                        continue
                    if '#' in absolute_url:
                        continue 
                    if absolute_url not in visited_urls and absolute_url not in urls_to_visit:
                        urls_to_visit.append(absolute_url)

            except Exception as e:
                print(f"Could not process {current_url} - Error: {e}")

    finally:
        print("\nClosing WebDriver...")
        driver.quit()

    generate_sitemap(visited_urls)

if __name__ == "__main__":
    main()
