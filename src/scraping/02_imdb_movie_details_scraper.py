import os 
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
from parsel import Selector
import httpx
import json

requests = httpx.Client(http2=True)

# Read the config file
def read_json(file_name):
    if not os.path.exists(file_name + 'program.json'):
        # If the data does not exist, initialize it
        initial_data = {
            'url_index': 0
        }
        with open(file_name + 'program.json', mode='w', encoding='utf-8') as f:
            json.dump(initial_data, f)
    with open(file_name + 'program.json', mode='r', encoding='utf-8') as f:
        # Load configuration data
        data = json.load(f)
        return data

# Write to the config file
def write_json(file_name, data):
    with open(file_name + 'program.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f)

def fetch_movie_details(url_: object) -> object:
    movies = []
    connect = ''
    if 'https://www.imdb.com/title/' in url_:
        pass
    else:
        return 'URL is incorrect'
    while not connect:
        try:
            response = requests.get(url_, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36'})
            connect = '1'
        except:
            # Retry the connection if it fails
            print('Connection closed {}'.format(url_))
    select = Selector(response.text)
    title = select.css('.hero__primary-text::text').get()  # Movie title
    if select.css('[data-testid="reviews-header"]'):
        full_url = select.css('[data-testid="reviews-header"]')[0].css('div > a')  # Full URL for reviews
    else:
        full_url = ''
    if full_url:
        full_url = 'https://www.imdb.com' + full_url.css('::attr(href)').get()
    else:
        full_url = 'No full URL available'
    if select.css('[data-testid="hero-rating-bar__aggregate-rating__score"]'):
        rating = select.css('[data-testid="hero-rating-bar__aggregate-rating__score"]')[0].css('span::text').getall()  # Rating
        rating = ''.join(rating)
    else:
        rating = 'No rating available'
    # Director information
    director = select.css('.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text')[0].get()
    # Box office details: gross worldwide, opening, and budget
    box_office = select.css('[data-testid="BoxOffice"]>div>ul>li')
    gross_worldwide = ''
    opening = ''
    budget = ''
    if box_office:
        for i in range(10):
            try:
                if box_office.css('span::text')[i].get() == 'Gross worldwide':
                    gross_worldwide = box_office.css('span::text')[i + 1].get()
                    continue
                if box_office.css('span::text')[i].get() == 'Opening weekend US & Canada':
                    opening1 = box_office.css('span::text')[i + 1].get()
                    opening2 = box_office.css('span::text')[i + 2].get()
                    opening = opening1 + ' · ' + opening2
                    continue
                if box_office.css('span::text')[i].get() == 'Budget':
                    budget = box_office.css('span::text')[i + 1].get()
                    continue
            except:
                continue
        if not gross_worldwide: gross_worldwide = 'No gross worldwide data'
        if not opening: opening = 'No opening data'
        if not budget: budget = 'No budget data'
    else:
        gross_worldwide = 'No gross worldwide data'
        opening = 'No opening data'
        budget = 'No budget data'
    
    # Writers information
    writers = ''
    writers_program = select.css('.ipc-metadata-list__item')
    for i in range(len(writers_program)):
        if writers_program[i].css('span::text').get() == 'Writers':
            writers = writers_program[i].css('div ul li a::text').getall()
            writers = ' · '.join(writers)
            break
        if writers_program[i].css('a::text').get() == 'Writers':
            writers = writers_program[i].css('div ul li a::text').getall()
            writers = ' · '.join(writers)
            break
        if writers_program[i].css('span::text').get() == 'Writer':
            writers = writers_program[i].css('div ul li a::text').getall()
            writers = ' · '.join(writers)
            break
        if writers_program[i].css('a::text').get() == 'Writer':
            writers = writers_program[i].css('div ul li a::text').getall()
            writers = ' · '.join(writers)
            break
    if not writers:
        writers = 'No writers data'
    
    # Language, country, filming locations, production, release date, official sites
    language = ''
    countries = ''
    filming = ''
    production = ''
    release_date = ''
    official_sites = ''
    Details_program = select.css('[data-testid="Details"] div ul.ipc-metadata-list--base li[data-testid]')
    for i in range(len(Details_program)):
        if Details_program[i].css('span::text').get() == 'Language':
            language = Details_program[i].css('div ul li a::text').get()
        if Details_program[i].css('span::text').get() == 'Languages':
            language = Details_program[i].css('div ul li a::text').getall()
            language = ' · '.join(language)
        if Details_program[i].css('span::text').get() == 'Countries of origin':
            countries = Details_program[i].css('div ul li a::text').getall()
            countries = ' · '.join(countries)
        if Details_program[i].css('a::text').get() == 'Filming locations':
            filming = Details_program[i].css('div ul li a::text').get()
        if Details_program[i].css('a::text').get() == 'Production companies':
            production = Details_program[i].css('div ul li a::text').getall()
            production = ' · '.join(production)
        if Details_program[i].css('a::text').get() == 'Release date':
            release_date = Details_program[i].css('div ul li a::text').getall()
            release_date = ' · '.join(release_date)
        if Details_program[i].css('a::text').get() == 'Official sites':
            official_sites = Details_program[i].css('div ul li a::text').getall()
            official_sites = ' · '.join(official_sites)
    if not language:
        language = 'No language data'
    if not countries:
        countries = 'No countries data'
    if not filming:
        filming = 'No filming data'
    if not production:
        filming = 'No production data'
    if not release_date:
        release_date = 'No release date data'
    if not official_sites:
        official_sites = 'No official sites data'
    movies.append({
        'title': title,
        'url': url_,
        'rating': rating,
        'director': director,
        'gross_worldwide': gross_worldwide,
        'opening': opening,
        'budget': budget,
        'writers': writers,
        'language': language,
        'countries': countries,
        'filming': filming,
        'production': production,
        'reviews_url': full_url,  # Add reviews URL
        'release_date': release_date,
        'official_sites': official_sites
    })
    return movies

def save_movies_to_csv(movies, filename):
    if not os.path.exists(filename):
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
            fieldnames = ['title', 'url', 'rating', 'director', 'gross_worldwide', 'opening', 'budget', 'writers', 'language',
                          'countries', 'filming', 'production', 'reviews_url', 'release_date', 'official_sites']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['title', 'url', 'rating', 'director', 'gross_worldwide', 'budget', 'opening', 'writers', 'language',
                      'countries', 'filming', 'production', 'reviews_url', 'release_date', 'official_sites']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for movie in movies:
            writer.writerow(movie)

if __name__ == '__main__':
    df = pd.read_excel(r"C:\Users\Tony.xie\Desktop\Online_Review_Project\Raw_Data\IMDB_Movie_URLs_1.xlsx")  # Path to the Excel file
    csv_filename = 'IMDd_Movie_detail_new.csv'  # Path to the CSV file
    config = read_json('config')  # Read JSON file to track the last processed URL
    for url in range(config['url_index'], len(df['URL'])):
        all_movies = []
        print(f'\r{len(df["URL"])} \ {config["url_index"] + 1} | {df["URL"][url]}', end='')
        movie_details = fetch_movie_details(df["URL"][url])
        if 'incorrect' in movie_details:
            config['url_index'] += 1
            write_json('config', config)
            continue
        all_movies.extend(movie_details)
        # Save data to CSV
        save_movies_to_csv(all_movies, csv_filename)
        config['url_index'] += 1
        write_json('config', config)
    print(f"\tMovie data has been saved to '{csv_filename}'")
