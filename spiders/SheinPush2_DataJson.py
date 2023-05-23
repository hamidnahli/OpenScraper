import requests
from bs4 import BeautifulSoup

http = 'https://www.shein.com/sitemap-index.xml'
r = requests.get(http)
soup = BeautifulSoup(r.text, 'xml')

site_map_link = [] #
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
            print(col.text)
            

for product in Product_link:                        # Get the data of product from Product_link
    #  product = 'https://shein.com/1pc-Carousel-Design-Candle-Holder-p-3462913-cat-3128.html'
     resp = requests.get(product)
     soup_product = BeautifulSoup(resp.text,'html.parser')
     print(soup_product)



for product in Product_link:
    result = requests.get(product)
    src = result.content
    soupa = BeautifulSoup(src,'lxml')

    #filtre scripts and soup only script which begin with 'window.goodsDetailV3SsrData'
    script = soupa.find("script", text=lambda text: text and 'window.goodsDetailV3SsrData' in text)

    #remove useless whitspace and tabs ...
    script_content = script.text.strip() 

    #filtre data from scripts
    start_index = script_content.find('{')                  #start from the first {
    end_index = script_content.rfind('html') + len('html')  #end on the last html word
    data_product_asJson = script_content[start_index:end_index]    #put the trimed script on data_product_asJson
    print(data_product_asJson)
    print('_______________________________________________________________________')
    print('_______________________________________________________________________')