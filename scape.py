import json
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Read data from the Excel file
excel_file = 'data.xlsx'  # Replace with your actual Excel file
data_frame = pd.read_excel(excel_file)

# Initialize a list to store scraped data
scraped_data = []

# Loop through the rows in the DataFrame
for index, row in data_frame.iterrows():
    url = f"https://www.amazon.{row['country']}/dp/{row['asin']}"

    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"{url} not available")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        product_title = soup.find('span', {'id': 'productTitle'}).get_text().strip()
        product_image_url = soup.find('img', {'id': 'landingImage'})['src']
        product_price = soup.find('span', {'id': 'priceblock_ourprice'}).get_text().strip()
        product_details = []
        for li in soup.find_all('li', {'class': 'a-list-item'}):
            product_details.append(li.get_text().strip())
        product_data = {
            'url': url,
            'title': product_title,
            'image_url': product_image_url,
            'price': product_price,
            'details': product_details
        }

        scraped_data.append(product_data)
        print(f"Scraped data for {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        continue

# Write scraped data to a JSON file
with open('scraped_data.json', 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4)
