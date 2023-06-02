from bs4 import BeautifulSoup
import requests
import pandas as pd 
infoProduct = []
for page in range(1,50):
  url = "https://www.jumia.ma/mlp-all-deals/" + "?page=" +str(page)+"#catalog-listing"
  url = requests.get(url)
  soup = BeautifulSoup(url.content , 'html.parser')
  products = soup.find_all('div' , class_ = 'info')

  for product in products:
      Name = product.find('h3' , class_="name").text.replace('\n', '')
      OriginalPrice = product.find('div' , class_= "prc").text.replace('\n', '')
      #OldPrice = product.find('div', class_= "old").text.replace('\n', '')
      try:
        Rating = product.find('div', class_='stars _s').text.replace('\n', '')
      except:
        Rating = 'None'
      infoProduct.append([ Name, OriginalPrice, Rating])
      #print(infoProduct)
df = pd.DataFrame(infoProduct)
df.to_excel('results.xlsx', index=False)
