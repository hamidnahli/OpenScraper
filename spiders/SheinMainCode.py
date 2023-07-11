import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import urllib.parse

http = 'https://www.shein.com/sitemap-index.xml'
r = requests.get(http)
soup = BeautifulSoup(r.text, 'xml')
datas = []
site_map_link = [] 
links = soup.find_all('loc')

for ele in links:
    if 'products' in ele.text:
        site_map_link.append(ele.text)
         
for collection in site_map_link:
    print('_____________________________________________________________________________')
    print(collection)
    print('_____________________________________________________________________________')
    rs = requests.get(collection)
    soup_collection = BeautifulSoup(rs.text, 'xml')
    collection_items = soup_collection.findAll('loc')
    
    for col in collection_items:
        if 'shein' in col.text:   
            link = col.text
            token = "f835ed1c6bee4260874b01ba5e3be5b0b2e7f1a7d65"
            targetUrl = urllib.parse.quote(link)
            geoCode = "us"
            api_link = "http://api.scrape.do?token={}&url={}&geoCode={}".format(token, targetUrl, geoCode)     
            resp = requests.get(api_link)
            soup_product = BeautifulSoup(resp.text, 'html.parser')
            script_element = soup_product.find("script", text=lambda text: text and 'window.goodsDetailV3SsrData' in text)
            
            if script_element is not None:
                script_content = script_element.text
                script = script_content.strip()
                first_line = script.splitlines()[0]
                start_index = first_line.find('{') 
                data_as_json = first_line[start_index:]
                parsed_data = json.loads(data_as_json)
                title_result = parsed_data["pageTitle"]
                page_title = title_result.split("|")[0].strip()
                price_dollar = parsed_data["productIntroData"]["getPrice"]["retailPrice"]["usdAmountWithSymbol"]

                data = {
                    "Title": page_title,
                    "Price": price_dollar,
                    "Link": link
                }

                datas.append(data)

            df = pd.DataFrame(datas)
            df.to_excel("Data.xlsx", index=False)