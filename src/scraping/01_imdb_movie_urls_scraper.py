from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function definition: Save data to Excel
def save_data_to_excel(data, file_path):
    df = pd.DataFrame(data, columns=['Release Group', 'URL'])
    df.to_excel(file_path, index=False)
    print(f"Data saved to {file_path}")

# Read the Excel file to get the list of movie names
excel_path = r"C:\Users\Box_Mojo_2007-2015.xlsx"
df = pd.read_excel(excel_path)
movie_names = df['Release Group'].tolist()

# Set up WebDriver
driver_path = '/Users/sathwik/Desktop/chromedriver.exe'
driver = webdriver.Chrome(driver_path)

try:
    driver.get("https://www.imdb.com/?ref_=nv_home")
    movie_urls = []

    # Search for each movie and get the URL of the first search result
    for movie_name in movie_names:
        search_box = driver.find_element(By.ID, 'suggestion-search')
        search_box.clear()
        search_box.send_keys(movie_name)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.react-autosuggest__suggestions-list'))
        )

        suggestions = driver.find_elements(By.CSS_SELECTOR, '.react-autosuggest__suggestion')
        if suggestions:
            suggestions[0].click()
            time.sleep(3)
            movie_urls.append((movie_name, driver.current_url))
        else:
            movie_urls.append((movie_name, "No URL found"))

finally:
    driver.quit()
    # Save the scraped data
    save_file_path = r"C:\Users\Online_Review_Project\Raw_Data\IMDB_Movie_URLs_1.xlsx"
    save_data_to_excel(movie_urls, save_file_path)
