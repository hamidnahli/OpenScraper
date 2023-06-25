from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl 


for all in range(1,2) :
    website = "https://www.amazon.com/s?k=gaming+laptop&crid=37IRAVD36API4&qid=1686656056&sprefix=gaming+la%2Caps%2C2174&ref=sr_pg_"+str(all)
    headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept-Language":"ar-MA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding":"gzip, deflate, br"
        }
    r = requests.get(website, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    div_element = soup.find_all('div',{'class':'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
    prodacts  = []
    for ele in div_element:
     
        title = ele.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text
        
        rating_element = ele.find('div',{'class':'a-row a-size-small'})
        if rating_element is not None :
             rating = (rating_element.text)
        else :
             rating = 'N/A'

        price = ele.find('span',{'class':'a-offscreen'}).text

        real_price_element = ele.find('span',{'class':'a-price a-text-price'})
        if real_price_element is not None :
            real_price = (real_price_element.text)
        else :
            real_price = 'N/A'
        
        delivery_price = ele.find('div',{'class':'a-row a-size-base a-color-secondary s-align-children-center'}).text
        if delivery_price is not None :
            delivery = (delivery_price)
        else :
            delivery = 'N/A'



        prodact = { 
            "Title" : title ,
            "Rating" : rating ,
            "Price" : price ,
            "Real Price" : real_price ,
            "Delivery price" : delivery_price ,
        }
    
        
        prodacts.append(prodact)

        df = pd.DataFrame(prodacts)

        df.to_excel('scraped_data.xlsx', index=False)