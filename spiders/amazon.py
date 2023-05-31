from bs4 import BeautifulSoup
import requests
import pandas as pd




website = "https://www.amazon.com/s?k=gaming+laptop&crid=5VA0UYIWTL90&sprefix=gaming+laptop%2Caps%2C200&ref=nb_sb_noss_1"

header = ({"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36","Accept-Language":"ar-MA,ar;q=0.9,en-US;q=0.8,en;q=0.7","Accept-Encoding":"gzip, deflate, br"})

r = requests.get(website, headers=header)



soup = BeautifulSoup(r.content, "html.parser")

result = soup.find_all("div",{"class":"a-section a-spacing-small a-spacing-top-small"})




for results in result :

    configuration = []
    try :
        configuration.append(results.find("span", {"class":"a-size-medium a-color-base a-text-normal"}).text)
    except :
        continue
    


    price = []
    try :
        price.append(results.find("span", {"class":"a-offscreen"}).text) 
    except :
        continue
    

    real_price = []
    try :
        real_price.append(results.find("span", {"class":"a-price a-text-price"}).text)
    except :
        continue
    


    delivery_price = []
    try :
        delivery_price.append(results.find("div", {"class":"a-row a-size-base a-color-secondary s-align-children-center"}).text)
    except :
        continue
    

    rating = []
    try :
        rating.append(results.find("div",{"class":"a-row a-size-small"}).text)   
    except :
        continue
    
    laptops = []
    
    laptop = ({"Configuration":configuration , "Price":price , "Real Price":real_price , "Delivery Price":delivery_price , "Rating":rating})
    laptops.append(laptop)

    df = pd.DataFrame(laptops)
    print(df.to_string(index=False).encode('utf-8'))
    
