# finploy-sitemap-generator
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Dynamic Sitemap Generator
A Python-based web crawler that automatically generates a sitemap.xml file for a given website.
This project uses Selenium and BeautifulSoup to crawl pages, extract internal links, and store them in sitemap format.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1.Crawls an entire website starting from a base URL.

2.Extracts internal links only (ignores external links & anchors).

3.Avoids duplicate URLs in the sitemap.

4.Generates a valid sitemap.xml file according to Sitemaps.org protocol.

5.Uses webdriver_manager to handle ChromeDriver automatically.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Tech Stack
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
* Python 3.x

* Selenium (for browser automation)

* BeautifulSoup (for HTML parsing)

* webdriver_manager (for managing ChromeDriver)

* urllib.parse (for URL handling)
  
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installation
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Clone the Repository
```
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2️. Install Dependencies
Make sure you have Python 3.x installed, then run:
```
pip install -r requirements.txt

````
Example requirements.txt:
```
beautifulsoup4
selenium
webdriver-manager

```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Usage
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Open url2.py
2. Change the base_url inside the main() function to your target website:
```
base_url = "https://www.example.com"
```
3. Run the script:
```
python url2.py
```
4. After crawling, the generated sitemap.xml will be saved in the project directory.
 --Example Output:
 ```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.finploy.com/jobs-in-other-dept-in-operations-central</loc>
    <lastmod>2025-08-09T16:26:29Z</lastmod>
  </url>
  <url>
    <loc>https://www.finploy.com/jobs-in-others-in-ma-advisory</loc>
    <lastmod>2025-08-09T16:26:29Z</lastmod>
  </url>
</urlset>
```
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How It Works
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1.Starts crawling from the base URL.

2.Uses Selenium to render pages (handles JavaScript-based sites).

3.Parses HTML with BeautifulSoup to find tags.

4.Converts relative links to absolute URLs.

5.Skips:
- External URLs
- Anchor (#) links
- Already visited pages

6.Writes the list of URLs to sitemap.xml.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Challenges & Solutions
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1.Challenge: Duplicate URLs being added. 
Solution: Used a set() for visited URLs.

2.Challenge: Some pages loaded slowly. 
Solution: Added a time.sleep(2) delay after each page load.

3.Challenge: Handling ChromeDriver setup. 
Solution: Used webdriver_manager to auto-install ChromeDriver.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Future Improvements
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1.Add multithreading for faster crawling.

2.Implement a headless mode for Chrome.

3.Add support for sitemap priorities and last modified dates.

4.Handle crawling depth limit for large websites.

