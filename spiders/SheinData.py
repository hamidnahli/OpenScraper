import requests
from bs4 import BeautifulSoup
import json
import time

http = 'https://www.shein.com/sitemap-index.xml'
r = requests.get(http)
soup = BeautifulSoup(r.text, 'xml')

site_map_link = [] 
linkprod = []
Product_link = []
category = []
useless_links = []
links = soup.find_all('loc')

for ele in links:                           # Filtrage links Products o lcategories o useless links
    if 'products' in ele.text:
         site_map_link.append(ele.text)
    elif 'category' in ele.text:
            category.append(ele.text)
    else:
         useless_links.append(ele.text)

i=0
for collection in site_map_link:                   # Get Product links from link
    print('_____________________________________________________________________________')
    print(collection)
    print('_____________________________________________________________________________')
    rs = requests.get(collection)
    soup_collection = BeautifulSoup(rs.text,'xml')
    collection_items = soup_collection.findAll('loc')
    for col in collection_items:
        if 'shein' in col.text:            
            Product_link.append(col.text)
            i+=1
            print("-----------------------------------------------")
            print('product number',i)
            resp = requests.get(col.text)
            soup_product = BeautifulSoup(resp.text,'html.parser')
                #filtre scripts and soup only script which begin with 'window.goodsDetailV3SsrData'
            script_content = soup_product.find("script", text=lambda text: text and 'window.goodsDetailV3SsrData' in text).text
                #remove useless whitspace and tabs ...
            script = script_content.strip()
                #let just the first line and bigin from the first '{'
            first_line = script.splitlines()[0]
            start_index = first_line.find('{') 
                #data as Json
            data_as_json = first_line[start_index:]
            #filltrage
            parsed_data = json.loads(data_as_json)
            title_result = parsed_data["pageTitle"]
            page_title = title_result.split("|")[0].strip() #remove '|' from the result
            
            print('Product Title is : ',page_title)
            price_dollar = parsed_data["productIntroData"]["getPrice"]["retailPrice"]["usdAmountWithSymbol"]
            print('Price of product is : ', price_dollar)