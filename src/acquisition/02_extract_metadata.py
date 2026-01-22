"""
IMDb Metadata Extraction Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A resilient scraper designed to extract high-dimensional metadata from IMDb 
movie pages. It implements idempotent execution logic (resume capability), 
robust error handling, and standardized data schemas.

Dependencies:
    - httpx (HTTP/2 Support)
    - parsel (CSS/XPath Selection)
    - tenacity (Retry Logic)
"""

import csv
import sys
from dataclasses import dataclass, fields, asdict
from pathlib import Path
from typing import Optional

import httpx
import pandas as pd
from parsel import Selector
from tenacity import retry, stop_after_attempt, wait_fixed

# --- Import from your new Utils Package ---
# Ensure your project root is in PYTHONPATH or run as module
try:
    from src.utils import setup_logger, clean_text
except ImportError:
    # Fallback for running script directly without package context (Not recommended but helpful for debugging)
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from src.utils import setup_logger, clean_text

# Initialize Professional Logger
logger = setup_logger(__name__)


# --- 1. Define Data Schema ---
@dataclass
class MovieMetadata:
    """Standardized Schema for Movie Metadata."""
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


# --- 2. Main Scraper Class ---
class IMDbMetadataExtractor:
    """
    Handles the lifecycle of fetching and parsing IMDb movie pages.
    """

    def __init__(self):
        # Enable HTTP/2 for better performance and lower detection risk
        self.client = httpx.Client(
            http2=True, 
            timeout=10.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }
        )

    @staticmethod
    def _extract_box_office(selector: Selector, label: str) -> str:
        """
        Private helper to extract specific box office metrics based on label text.
        
        Args:
            selector: The Parsel selector for the whole page.
            label: The visible label text (e.g., 'Gross worldwide').
        """
        # Robust XPath: Find the <li> that contains a <span> with the specific label
        item = selector.xpath(f'//li[descendant::span[text()="{label}"]]')
        if not item:
            return "N/A"
        
        # Extract the value, usually in the subsequent span or list item content
        value = item.css('span.ipc-metadata-list-item__list-content-item::text').get()
        return clean_text(value)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_page(self, url: str) -> Optional[Selector]:
        """Fetches the URL with automatic retries."""
        if 'imdb.com/title/' not in url:
            logger.warning(f"Skipping invalid URL format: {url}")
            return None
        
        try:
            response = self.client.get(url)
            response.raise_for_status() # Raises httpx.HTTPStatusError for 4xx/5xx
            return Selector(text=response.text)
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error fetching {url}: {e}")
            raise # Let tenacity handle the retry

    def parse(self, url: str, selector: Selector) -> MovieMetadata:
        """
        Parses the HTML selector to populate the MovieMetadata schema.
        Using the central 'clean_text' utility ensures consistency.
        """
        data = MovieMetadata(url=url)
        
        # --- Basic Info ---
        data.title = clean_text(selector.css('.hero__primary-text::text').get())
        data.rating = clean_text(selector.css('[data-testid="hero-rating-bar__aggregate-rating__score"] span::text').get())
        
        # --- Credits (List Handling) ---
        # Note: clean_text handles None implicitly, but for lists we join them first
        data.director = clean_text(' · '.join(selector.css('li:contains("Director") .ipc-metadata-list-item__list-content-item::text').getall()))
        data.writers = clean_text(' · '.join(selector.css('li:contains("Writer") .ipc-metadata-list-item__list-content-item::text').getall()))
        
        # --- Box Office ---
        data.gross_worldwide = self._extract_box_office(selector, 'Gross worldwide')
        data.budget = self._extract_box_office(selector, 'Budget')
        data.opening_weekend = self._extract_box_office(selector, 'Opening weekend US & Canada')

        # --- Details Section ---
        data.languages = clean_text(' · '.join(selector.css('[data-testid="title-details-languages"] a::text').getall()))
        data.countries = clean_text(' · '.join(selector.css('[data-testid="title-details-origin"] a::text').getall()))
        data.production_companies = clean_text(' · '.join(selector.css('[data-testid="title-details-companies"] a::text').getall()))
        data.release_date = clean_text(' · '.join(selector.css('[data-testid="title-details-releasedate"] a::text').getall()))
        data.filming_locations = clean_text(' · '.join(selector.css('[data-testid="title-details-filminglocations"] a::text').getall()))

        # --- Reviews URL Logic ---
        reviews_endpoint = selector.css('[data-testid="reviews-header"] a::attr(href)').get()
        if reviews_endpoint:
             # Ensure we don't double slash
            data.reviews_url = f"https://www.imdb.com{reviews_endpoint}"
        
        return data

    def run_pipeline(self, input_path: Path, output_path: Path):
        """
        Executes the main scraping pipeline with Idempotency (Resume capability).
        """
        if not input_path.exists():
            logger.critical(f"Input file not found: {input_path}")
            return

        # 1. Load Tasks
        df = pd.read_excel(input_path)
        if 'URL' not in df.columns:
            logger.critical("Input Excel is missing the required 'URL' column.")
            return
        
        urls = df['URL'].dropna().tolist()
        
        # 2. Idempotency Check (Load existing progress)
        processed_urls = set()
        if output_path.exists():
            try:
                # Optimized read: only load the 'url' column to save memory
                existing_df = pd.read_csv(output_path, usecols=['url'])
                processed_urls = set(existing_df['url'].tolist())
                logger.info(f"Resume Check: Found {len(processed_urls)} movies already scraped.")
            except Exception as e:
                logger.warning(f"Could not read existing checkpoint: {e}. Starting fresh.")

        # 3. Processing Loop
        # Open in append mode ('a') so we save progress in real-time
        write_header = not output_path.exists()
        
        with open(output_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(MovieMetadata)])
            
            if write_header:
                writer.writeheader()

            total_tasks = len(urls)
            logger.info(f"Starting pipeline. Tasks remaining: {total_tasks - len(processed_urls)}")

            for i, url in enumerate(urls):
                if url in processed_urls:
                    continue
                
                # Simple progress indicator to console (using \r to update line)
                sys.stdout.write(f"\r[Processing] {i+1}/{total_tasks} | {url[:50]}...")
                sys.stdout.flush()

                try:
                    selector = self.fetch_page(url)
                    if selector:
                        movie_data = self.parse(url, selector)
                        writer.writerow(asdict(movie_data))
                        f.flush() # Ensure data is written to disk immediately
                except Exception as e:
                    logger.error(f"\nFailed to process {url}: {e}")

        logger.info(f"\nPipeline complete. Data saved to {output_path}")

if __name__ == "__main__":
    # --- Configuration for Execution ---
    # Define paths relative to this script or project root
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    
    # Define Input/Output (Assuming the new directory structure)
    INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "urls" / "IMDB_Movie_URLs.xlsx"
    OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "metadata" / "IMDb_Movie_Details.csv"

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    scraper = IMDbMetadataExtractor()
    scraper.run_pipeline(INPUT_FILE, OUTPUT_FILE)