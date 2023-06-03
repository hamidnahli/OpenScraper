from bs4 import BeautifulSoup
import requests
import pandas as pd


website = "https://www.amazon.com/s?k=gaming+laptop&crid=5VA0UYIWTL90&sprefix=gaming+laptop%2Caps%2C200&ref=nb_sb_noss_1"

headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language":"ar-MA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding":"gzip, deflate, br"
        }

r = requests.get(website, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

div_element = soup.find_all('div',{'class':'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
print(len(div_element))
for ele in div_element:

    title = []
    title.append(ele.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text)

    rating = []
    rating_element = ele.find('div',{'class':'a-row a-size-small'})
    if rating_element is not None :
        rating.append(rating_element.text)
    else :
         rating.append('N/A')

    price = []
    price.append(ele.find('span',{'class':'a-offscreen'}).text)
    
    real_price = []
    real_price_element = ele.find('span',{'class':'a-price a-text-price'})
    if real_price_element is not None :
        real_price.append(real_price_element.text)
    else :
        real_price.append('N/A') 

    delivery_price = []
    delivery_price.append(ele.find('div',{'class':'a-row a-size-base a-color-secondary s-align-children-center'}).text)
    
    gaming_laptop = pd.DataFrame({'Confuguration':title,'Rating':rating,'Price':price,'Rreal Price':real_price,'Delivery Price':delivery_price})
    #print(gaming_laptop.to_string().encode('utf-8', errors='replace'))



