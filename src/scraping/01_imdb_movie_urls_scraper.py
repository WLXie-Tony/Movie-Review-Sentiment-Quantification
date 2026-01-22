"""
IMDb Movie URL Scraper
Author: Wenlan Xie
Description: Retrieves IMDb URLs for a list of movies using Selenium automation.
"""

import time
import logging
from pathlib import Path
from typing import List, Tuple, Optional
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IMDbURLFetcher:
    def __init__(self, headless: bool = False):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        # Auto-install driver
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def search_movie(self, movie_name: str) -> str:
        """Searches for a movie and returns the first result URL."""
        base_url = "https://www.imdb.com/?ref_=nv_home"
        try:
            self.driver.get(base_url)
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'suggestion-search'))
            )
            search_box.clear()
            search_box.send_keys(movie_name)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.react-autosuggest__suggestions-list'))
            )
            
            suggestions = self.driver.find_elements(By.CSS_SELECTOR, '.react-autosuggest__suggestion')
            if suggestions:
                suggestions[0].click()
                # Wait for URL to change or page to load
                time.sleep(2) 
                return self.driver.current_url
            else:
                logger.warning(f"No suggestions found for: {movie_name}")
                return "No URL found"

        except Exception as e:
            logger.error(f"Error searching for {movie_name}: {e}")
            return "Error"

    def process_excel(self, input_path: str, output_path: str):
        input_file = Path(input_path)
        output_file = Path(output_path)
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        df = pd.read_excel(input_file)
        if 'Release Group' not in df.columns:
            raise ValueError("Input Excel must contain a 'Release Group' column.")
            
        movie_names = df['Release Group'].dropna().unique().tolist()
        results = []

        logger.info(f"Starting scraping for {len(movie_names)} movies...")
        
        for name in movie_names:
            url = self.search_movie(name)
            results.append({'Release Group': name, 'URL': url})
            logger.info(f"Processed: {name} -> {url}")

        output_df = pd.DataFrame(results)
        output_df.to_excel(output_file, index=False)
        logger.info(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    # Configuration
    INPUT_FILE = "./data/Box_Mojo_2007-2015.xlsx"  # Use relative paths!
    OUTPUT_FILE = "./data/IMDB_Movie_URLs.xlsx"
    
    # Ensure data directory exists
    Path("./data").mkdir(exist_ok=True)

    with IMDbURLFetcher(headless=False) as fetcher:
        fetcher.process_excel(INPUT_FILE, OUTPUT_FILE)
