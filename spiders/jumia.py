import requests
from bs4 import BeautifulSoup

url = 'https://www.jumia.ma/mlp-boutique-officielle-adidas/'
html_file = requests.get(url).text
soup = BeautifulSoup(html_file, 'html.parser')
data_category = 'Health & Beauty/Personal Care/Bath & Bathing Accessories'
product_titles = soup.find_all('a', class_='core')
for title in product_titles:
    print(title.text.strip(' '))