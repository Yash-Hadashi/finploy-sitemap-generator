from urllib.parse import urljoin, urlparse
from collections import deque
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import logging

START_URL = "https://www.finploy.com"
OUTPUT_FILE = "sitemap.xml"
HEADLESS = True  # True to hide browser, False to see it
DELAY = 0.6       # seconds between page loads
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def is_same_domain(start_netloc, url):
    return urlparse(url).netloc.endswith(start_netloc)


def normalize_url(base, href):
    if not href or href.startswith(("javascript:", "mailto:", "tel:")):
        return None
    href = href.split("#")[0].strip()
    if not href:
        return None
    return urljoin(base, href)


def create_driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,1024")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver


def expand_jobs_by_location(driver, wait=0.6):
    """Expand 'Jobs by location' section and return all found location links."""
    logging.info("Expanding 'Jobs by location' View More buttons...")
    driver.get(START_URL)
    time.sleep(wait * 1.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(wait)

    clicks = 0
    while True:
        try:
            btns = driver.find_elements(By.XPATH, "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'view more')] | //a[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'view more')]")
            btns = [b for b in btns if b.is_displayed()]
            if not btns:
                break
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btns[0])
            time.sleep(0.3)
            btns[0].click()
            clicks += 1
            time.sleep(wait)
            if clicks > 50:
                break
        except:
            break

    soup = BeautifulSoup(driver.page_source, "lxml")
    links = set()
    for a in soup.find_all("a", href=True):
        full = normalize_url(START_URL, a["href"])
        if full:
            links.add(full)
    logging.info(f"Found {len(links)} location links.")
    return links


def extract_links_from_html(base_url, html):
    soup = BeautifulSoup(html, "lxml")
    links = set()
    for a in soup.find_all("a", href=True):
        full = normalize_url(base_url, a["href"])
        if full:
            links.add(full)
    return links


def crawl_site():
    driver = create_driver()
    visited = set()
    queue = deque()

    
    location_links = expand_jobs_by_location(driver, wait=DELAY)
    queue.append(START_URL)
    for link in location_links:
        queue.append(link)

    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        try:
            driver.get(url)
        except:
            continue
        time.sleep(DELAY)
        page_html = driver.page_source
        for link in extract_links_from_html(url, page_html):
            if is_same_domain(urlparse(START_URL).netloc, link) and link not in visited:
                queue.append(link)
        visited.add(url)
        logging.info(f"Crawled: {url} (Total: {len(visited)})")

    driver.quit()
    return list(visited)


def generate_sitemap(urls):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write("  <url>\n")
            f.write(f"    <loc>{u}</loc>\n")
            f.write(f"    <lastmod>{now}</lastmod>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")
    logging.info(f"Sitemap saved to {OUTPUT_FILE} with {len(urls)} URLs.")


if __name__ == "__main__":
    urls = crawl_site()
    generate_sitemap(urls)

