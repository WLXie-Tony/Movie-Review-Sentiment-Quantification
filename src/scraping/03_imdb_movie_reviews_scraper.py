import xlwt
import pandas as pd
import httpx
from bs4 import BeautifulSoup
import time
requests = httpx.Client(http2=True)
import re
import execjs

# Read the Excel file containing URLs
combined_df = pd.read_csv(r"C:\Users\Online_Review_Project\Raw_Data\IMDd_Movie_detail_new.csv")

def call_js(filename, func_name, *args):
    with open(filename, 'r', encoding='utf-8') as f:
        js_code = execjs.compile(f.read())
    return js_code.call(func_name, *args)

# Create an Excel workbook and worksheet
f = xlwt.Workbook()
sheet1 = f.add_sheet('Movie Reviews', cell_overwrite_ok=True)
headers = ["Movie Title", "IMDb URL", "Movie Rating", "Director", "Box Office", "Opening Weekend", "Reviews URL",
           "Review Title", "Review Author", "Review Date", "Upvotes", "Total Votes", "Review Rating", "Review Content"]
for i, header in enumerate(headers):
    sheet1.write(0, i, header)

# Maximum number of reviews
MAX_CNT = 5000

# Initialize the counter
cnt = 1

# Request data from the API
def send_data(target_url, cnt_, paginationKey, ue_id, MAX_cnt_):
    data_key_ = ''
    print("paginationKey:", paginationKey)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    }
    cookies = {
        "uu": "eyJpZCI6InV1ODMyYzUyNTViZWQ0NDY2NzhmN2EiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=",
        "session-id": "140-8033594-1760024",
        "session-id-time": "2341114482",
        "ubid-main": "135-4128638-6075920",
        "session-token": "aotp91utm73+0rVyA3SPFXQW7H4ENJjcHrW8vzFV3ZVZ2gpi5mxGXPm1D8etglmdAcVgZO9RVyXuA7nIeWeGJqKCY6E31BINAle07Q25BsEymoFx5yEY6OeqmLhilYRg+DkBa6azkmut9332DYklqngOs2209P+25ekbAOGA9JS3JfyaW6HVZ3dhbjX3J4DGfEs/qJ2JZikdH/o3xQgxp/A4Zru1g+SqR7CYECMQWS4EVacOSYTrOb6BcY5OPXrGdf74Amra5LdeEGO4JDfyitxCqi4hoFNeRz/g+rcRYs7+IgMV+bXYXyeNGxQgjoB8g53jRxKhtLUDjZCcbaVfpZpCLt6orMZY",
        "ci": "e30",
        'csm-hit': call_js('tracking_token_generator.js', 'sdk', ue_id)
    }
    url = f"https://www.imdb.com/title/{target_url.split('/')[4]}/reviews/_ajax"
    # This URL is not being replaced properly; the send_data function keeps visiting the same URL
    params = {
        "ref_": "undefined",
        "paginationKey": paginationKey
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    soup = BeautifulSoup(response.text, "lxml")
    for item in soup.select(".lister-item-content"):
        title = item.select_one(".title").text.strip() if item.select_one(".title") else ""
        author = item.select_one(".display-name-link").text.strip() if item.select_one(".display-name-link") else ""
        date = item.select_one(".review-date").text.strip() if item.select_one(".review-date") else ""
        votetext = item.select_one(".text-muted").text.strip() if item.select_one(".text-muted") else ""
        votes = re.findall(r"\d+", votetext)
        upvote = votes[0] if votes else ""
        totalvote = votes[1] if len(votes) > 1 else ""
        review_rating = item.select_one("span.rating-other-user-rating > span").text.strip() if item.select_one(
            "span.rating-other-user-rating > span") else ""
        review_content = item.select_one(".text").text.strip() if item.select_one(".text") else ""
        print('review_content:', review_content)
        row_data = [movie_title, imdb_url, movie_rating, director, gross, opening, reviews_url, title, author, date,
                    upvote, totalvote, review_rating, review_content]
        if soup.select(".load-more-data"):
            data_key_ = soup.select(".load-more-data")[0].get('data-key')
        for i, data in enumerate(row_data):
            sheet1.write(cnt_, i, data)
        cnt_ += 1
        if cnt_ >= MAX_cnt_:
            break
    return cnt_, data_key_

# Iterate through each URL
for index, row in combined_df.iterrows():
    # Read additional information from the original Excel file
    movie_title = row['Title']
    imdb_url = row['URL']
    movie_rating = row['Rating']
    director = row['Director']
    gross = row['Gross_worldwide']
    opening = row['Opening weekend US & Canada']
    reviews_url = row['Reviews_url']

    print("Scraping URL:", reviews_url)

    while reviews_url and cnt < MAX_CNT:
        print("url = ", reviews_url)
        res = requests.get(reviews_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "lxml")
        ueid = re.findall("ue_id = '(.*?)',", res.text)
        if ueid:
            ueid = ueid[0]
        time.sleep(3)
        for item in soup.select(".lister-item-content"):
            title = item.select_one(".title").text.strip() if item.select_one(".title") else ""
            author = item.select_one(".display-name-link").text.strip() if item.select_one(".display-name-link") else ""
            date = item.select_one(".review-date").text.strip() if item.select_one(".review-date") else ""
            votetext = item.select_one(".text-muted").text.strip() if item.select_one(".text-muted") else ""
            votes = re.findall(r"\d+", votetext)
            upvote = votes[0] if votes else ""
            totalvote = votes[1] if len(votes) > 1 else ""
            review_rating = item.select_one("span.rating-other-user-rating > span").text.strip() if item.select_one(
                "span.rating-other-user-rating > span") else ""
            review_content = item.select_one(".text").text.strip() if item.select_one(".text") else ""
            data_key = ''
            if soup.select(".load-more-data"):
                data_key = soup.select(".load-more-data")[0].get('data-key')
            row_data = [movie_title, imdb_url, movie_rating, director, gross, opening, reviews_url, title, author, date,
                        upvote, totalvote, review_rating, review_content]
            for i, data in enumerate(row_data):
                sheet1.write(cnt, i, data)
            cnt += 1

            if cnt >= MAX_CNT:
                break
        print('Counter value 1: ', cnt)
        for i in range(3):  # Specify the number of review pages to fetch; range(1) means 1*50 reviews, etc.
            if data_key:
                cnt, data_key = send_data(reviews_url, cnt, data_key, ueid, MAX_CNT)  # Append additional data
                print(f'Counter value for {i}: ', cnt)
        load_more = soup.select_one(".load-more-data")
        if load_more and 'data-key' in load_more.attrs:
            key = load_more['data-key']
            if 'data-ajaxurl' in load_more.attrs:
                ajaxurl = load_more['data-ajaxurl']
                next_page_url = "https://www.imdb.com" + ajaxurl + "?ref_=undefined&paginationKey=" + key
                reviews_url = next_page_url  # Update reviews_url to access the next page
            else:
                reviews_url = None  # No next page
        else:
            reviews_url = None  # No more pages or data keys

# Save the Excel file
f.save('IMDb_Reviews_with_Details.xls')
print(cnt, "reviews and their details have been saved.")
