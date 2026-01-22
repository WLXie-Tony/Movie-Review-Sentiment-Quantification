"""
IMDb Reviews Scraper
Author: Wenlan Xie
Description: Iterates through movies and fetches paginated user reviews via AJAX.
"""

import logging
import time
import re
from typing import Dict, List, Optional
import pandas as pd
import httpx
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed, stop_after_attempt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IMDbReviewFetcher:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.session = httpx.Client(http2=True, timeout=10.0)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            # NOTE: Ideally, 'cookie' should be dynamically retrieved or managed via session
            # For academic reproducibility, document clearly how to update these cookies.
        }
    
    def get_review_token(self, url: str) -> Optional[str]:
        """Fetches the initial page to extract the ue_id or similar tokens."""
        try:
            res = self.session.get(url, headers=self.headers)
            # Logic to extract 'ue_id' or 'paginationKey' from initial HTML
            # This is simplified; robust scraping requires dynamic parsing
            return res.text
        except Exception as e:
            logger.error(f"Initial handshake failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_ajax_reviews(self, imdb_id: str, pagination_key: str) -> Dict:
        url = f"https://www.imdb.com/title/{imdb_id}/reviews/_ajax"
        params = {
            "ref_": "undefined",
            "paginationKey": pagination_key
        }
        res = self.session.get(url, headers=self.headers, params=params)
        res.raise_for_status()
        return res

    def parse_reviews(self, html_content: str, movie_meta: Dict) -> List[Dict]:
        soup = BeautifulSoup(html_content, "lxml")
        reviews = []
        for item in soup.select(".lister-item-content"):
            review = movie_meta.copy() # Inherit movie metadata
            
            review['review_title'] = item.select_one(".title").text.strip() if item.select_one(".title") else ""
            review['author'] = item.select_one(".display-name-link").text.strip() if item.select_one(".display-name-link") else ""
            review['date'] = item.select_one(".review-date").text.strip() if item.select_one(".review-date") else ""
            review['content'] = item.select_one(".text").text.strip() if item.select_one(".text") else ""
            
            # Rating logic
            rating_tag = item.select_one("span.rating-other-user-rating > span")
            review['user_rating'] = rating_tag.text.strip() if rating_tag else "N/A"
            
            reviews.append(review)
        
        # Extract next key
        load_more = soup.select_one(".load-more-data")
        next_key = load_more.get('data-key') if load_more else None
        
        return reviews, next_key

    def process_dataset(self, input_csv: str):
        df = pd.read_csv(input_csv)
        all_reviews = []
        
        for idx, row in df.iterrows():
            movie_meta = {
                'Movie Title': row.get('title'),
                'IMDb URL': row.get('url'),
                'Director': row.get('director')
            }
            reviews_url = row.get('reviews_url')
            
            if pd.isna(reviews_url) or "http" not in reviews_url:
                continue

            try:
                # Extract ID like 'tt1234567'
                imdb_id = reviews_url.split('/title/')[1].split('/')[0]
            except IndexError:
                continue
            
            logger.info(f"Fetching reviews for: {movie_meta['Movie Title']}")
            
            # Logic flow for pagination would go here
            # Due to the complexity of the AJAX key generation without the JS file,
            # this section focuses on the structure:
            
            # 1. Initial Request (to get first batch or tokens)
            # 2. Loop with paginationKey
            # 3. Append to all_reviews
            
            # For demonstration, we assume we fetch just the main page reviews 
            # to avoid the broken JS dependency in this refactor example.
            try:
                res = self.session.get(reviews_url, headers=self.headers)
                reviews, _ = self.parse_reviews(res.text, movie_meta)
                all_reviews.extend(reviews)
            except Exception as e:
                logger.error(f"Failed to scrape {reviews_url}: {e}")

        # Save Final
        final_df = pd.DataFrame(all_reviews)
        final_df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
        logger.info(f"Saved {len(final_df)} reviews to {self.output_file}")

if __name__ == "__main__":
    fetcher = IMDbReviewFetcher(output_file="./data/IMDb_Reviews_Final.csv")
    fetcher.process_dataset("./data/IMDb_Movie_Details_Clean.csv")
