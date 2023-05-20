import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.shein.com/sitemap-index.xml')
soup = BeautifulSoup(r.text, 'xml')

link = []
linkprod = []
products = []
links = soup.find_all('loc')

for ele in range(len(links)):
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    link.append(links[ele].text)
    # print(link[ele])

    for linkprod in link:
        # print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        rs = requests.get(linkprod)
        soup_prod = BeautifulSoup(rs.text, 'xml')
        linkprod_items = soup_prod.find_all('loc')
        products.append(linkprod_items[0].text)
        # print(products)

print('------------------------------------------------------')
print(link)
print('______________________________________________________')
print(products)
git add .
git commit -m "scrap all Shein's product using Sitemap"