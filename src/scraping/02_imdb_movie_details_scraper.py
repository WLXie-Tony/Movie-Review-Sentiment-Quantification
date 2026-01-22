"""
IMDb Details Extractor
Author: Wenlan Xie
Description: High-performance scraper using HTTPX and Parsel to extract metadata.
"""

import csv
import logging
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Optional, Dict, Any

import httpx
import pandas as pd
from parsel import Selector
from tenacity import retry, stop_after_attempt, wait_fixed

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 1. Define Data Schema (The "Academic" Way) ---
@dataclass
class MovieMetadata:
    title: str = "N/A"
    url: str = "N/A"
    rating: str = "N/A"
    director: str = "N/A"
    gross_worldwide: str = "N/A"
    opening_weekend: str = "N/A"
    budget: str = "N/A"
    writers: str = "N/A"
    languages: str = "N/A"
    countries: str = "N/A"
    filming_locations: str = "N/A"
    production_companies: str = "N/A"
    release_date: str = "N/A"
    reviews_url: str = "N/A"

# --- 2. Helper Logic ---
class ScraperUtils:
    @staticmethod
    def clean_text(text_list: list) -> str:
        """Joins a list of strings cleanly."""
        if not text_list:
            return "N/A"
        return ' · '.join([t.strip() for t in text_list if t.strip()])

    @staticmethod
    def get_box_office(selector: Selector, label: str) -> str:
        """Robust extraction for Box Office list items."""
        # Find the li element that contains the specific span label
        item = selector.xpath(f'//li[descendant::span[text()="{label}"]]')
        if not item:
            return "N/A"
        # Extract the value (usually in the span following the label or direct text)
        value = item.css('span.ipc-metadata-list-item__list-content-item::text').get()
        return value if value else "N/A"

# --- 3. Main Scraper Class ---
class IMDbDetailScraper:
    def __init__(self):
        self.client = httpx.Client(http2=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        })

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_page(self, url: str) -> Optional[Selector]:
        if 'imdb.com/title/' not in url:
            logger.warning(f"Invalid URL skipped: {url}")
            return None
        
        response = self.client.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch {url}: Status {response.status_code}")
            raise Exception("Network Error")
        return Selector(text=response.text)

    def parse_details(self, url: str, selector: Selector) -> MovieMetadata:
        data = MovieMetadata(url=url)
        
        # Basic Info
        data.title = selector.css('.hero__primary-text::text').get(default="N/A")
        data.rating = selector.css('[data-testid="hero-rating-bar__aggregate-rating__score"] span::text').get(default="N/A")
        
        # Credits
        data.director = ScraperUtils.clean_text(selector.css('li:contains("Director") .ipc-metadata-list-item__list-content-item::text').getall())
        data.writers = ScraperUtils.clean_text(selector.css('li:contains("Writer") .ipc-metadata-list-item__list-content-item::text').getall())
        
        # Box Office (Logic simplified for readability)
        data.gross_worldwide = ScraperUtils.get_box_office(selector, 'Gross worldwide')
        data.budget = ScraperUtils.get_box_office(selector, 'Budget')
        data.opening_weekend = ScraperUtils.get_box_office(selector, 'Opening weekend US & Canada')

        # Details Section
        data.languages = ScraperUtils.clean_text(selector.css('[data-testid="title-details-languages"] a::text').getall())
        data.countries = ScraperUtils.clean_text(selector.css('[data-testid="title-details-origin"] a::text').getall())
        data.production_companies = ScraperUtils.clean_text(selector.css('[data-testid="title-details-companies"] a::text').getall())
        data.release_date = ScraperUtils.clean_text(selector.css('[data-testid="title-details-releasedate"] a::text').getall())
        data.filming_locations = ScraperUtils.clean_text(selector.css('[data-testid="title-details-filminglocations"] a::text').getall())

        # Review URL construction
        reviews_endpoint = selector.css('[data-testid="reviews-header"] a::attr(href)').get()
        data.reviews_url = f"https://www.imdb.com{reviews_endpoint}" if reviews_endpoint else "N/A"

        return data

    def run(self, input_excel: str, output_csv: str):
        input_path = Path(input_excel)
        output_path = Path(output_csv)
        
        # Load input
        df = pd.read_excel(input_path)
        urls = df['URL'].tolist()
        
        # Check existing to resume
        processed_urls = set()
        if output_path.exists():
            existing_df = pd.read_csv(output_path)
            processed_urls = set(existing_df['url'].tolist())
            logger.info(f"Resuming... {len(processed_urls)} movies already scraped.")

        # Open CSV for appending
        write_header = not output_path.exists()
        with open(output_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(MovieMetadata)])
            if write_header:
                writer.writeheader()

            for i, url in enumerate(urls):
                if url in processed_urls:
                    continue
                
                print(f"Processing {i+1}/{len(urls)}: {url}", end='\r')
                try:
                    sel = self.fetch_page(url)
                    if sel:
                        movie_data = self.parse_details(url, sel)
                        writer.writerow(vars(movie_data))
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")

if __name__ == "__main__":
    scraper = IMDbDetailScraper()
    scraper.run(
        input_excel="./data/IMDB_Movie_URLs.xlsx", 
        output_csv="./data/IMDb_Movie_Details_Clean.csv"
    )
