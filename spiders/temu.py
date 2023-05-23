# Tech stack:
# Selenium, Playwright, httpx, Scrapy, requests
# BS4, lxml, re
# pandas


# requests
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
r = requests.get(
    'https://www.temu.com/no-tie-shoe-laces-lazy-elastic-shoelaces-metal-capsule-button-for-any-kids-adult-shoes-g-601099513834171.html?top_gallery_url=https%3A%2F%2Fimg.kwcdn.com%2Fproduct%2Fopen%2F2023-01-25%2F1674625637420-3d6af0ad998b48ffa3b36fe85358ffff-goods.jpeg&spec_gallery_id=13583504&refer_page_sn=10463&refer_source=0&freesia_scene=312&_oak_freesia_scene=312&refer_page_el_sn=207184&_x_channel_scene=spike&_x_channel_src=1&_x_sessn_id=e7zi0hwhwd&refer_page_name=exclusive-offer&refer_page_id=10463_1684277156137_9941m2plb7',
    headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

title = soup.find('div', {'class': '_2rn4tqXP'}).text
price_tag = soup.find('div', {'class': '_15o2bYpT'})
prices = price_tag.findAll('div')
sale_price = prices[0].text
original_price = prices[1].text
sales = prices[2].text
image_container = soup.find('div', {'class': '_qc4rnOX'})
images = image_container.findAll('div')


reviews_count = soup.find('div', {'class': '_3ZiVVHzx'}).text.replace(' reviews', '')
brand = soup.find('div', {'class': '_3eJGEFuW'}).text
sold = soup.find('div', {'class': '_1FfJhhv_'}).text
sold_by_brand = soup.find('div', {'class': 'WSu-sds6'}).text


