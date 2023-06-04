import time

from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils.coingecko import parse_product, check_login_stock

load_dotenv()


def start_browser(p):
    browser = p.firefox.launch(
        headless=False,
        proxy={
            "server": 'https://proxy.packetstream.io:31111',
            "username": 'hnmedia',
            "password": 'puwpvA0vsZ8zo0l5'
        }
    )
    context = browser.new_context(java_script_enabled=False)
    context.route('**/*',
                  lambda route, request: route.abort() if request.resource_type == 'image' else route.continue_())
    page = context.new_page()
    return page, browser


def scrap_url(p):
    page, browser = start_browser(p)
    page.goto('https://www.temu.com/channel/best-sellers.html')
    html = page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.findAll('a', {'class': '_3VEjS46S _2IVkRQY-'})
    urls = ['https://www.temu.com' + url['href'] for url in urls]

    browser.close()
    return urls


with sync_playwright() as p:
    urls = scrap_url(p)
    for url in urls:
        try:
            page, browser = start_browser(p)
            page.goto(url)
            page.wait_for_selector('xpath=//div[contains(@class, "_2rn4tqXP")]', timeout=60000)
            html = page.inner_html('body')
            soup = BeautifulSoup(html, 'html.parser')
            product_info = parse_product(soup)
            print(product_info)
            browser.close()

        except Exception as e:
            browser.close()
            print(f'{e}: {url}')

# recursion

# New approach: Open every product in new tab.

# nothing shows up!!!! -> if title.text == None -> redo request
# request falls under login (Bad IP) -> redo the request
# sold out -> redo the request.
# if product is really out of stock -> # wait until fall under it.


"""
issue: slow page load due to bad proxy
- skip image load
- refresh new proxy

Issue: login pop up while looping through product urls

### API ENDPINT

# Returns list of bought together for a product ID
https://www.temu.com/api/poppy/v1/goods_detail?scene=goods_detail_bought_together


# Returns list of similar products for a product ID
https://www.temu.com/api/poppy/v1/goods_detail?scene=goods_detail_similar

# 
https://www.temu.com/api/poppy/v1/goods_detail?scene=goods_detail_like
"""

headers = {

    'Host': 'www.temu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'region=211; language=en; currency=USD; api_uid=Cmy3GmRy2c9HZwB7rb4BAg==; timezone=America%2FChicago; _nano_fp=XpEJnpPYl0Tjn5TjnC_6~lg4lHDJOrYV9zAXiXKl; webp=1; shipping_city=211%2C211000000025949; _bee=sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa; njrpl=sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa; dilx=Olpu1R6JAoW6OApDTrBYF; hfsc=L32CfYs04Tr+1JLOfg==; goods=goods_erggvh'
}

_bee
"sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa"
_nano_fp
"XpEJnpPYl0Tjn5TjnC_6~lg4lHDJOrYV9zAXiXKl"
api_uid
"Cmy3GmRy2c9HZwB7rb4BAg=="
currency
"USD"
dilx
"Olpu1R6JAoW6OApDTrBYF"
goods
"goods_hx37m4"
hfsc
"L32CfYs04Tr+1JLOfg=="
language
"en"
njrpl
"sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa"
region
"211"
shipping_city
"211,211000000025949"
timezone
"America/Chicago"
webp
"1"

_bee
"sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa"
_nano_fp
"XpEJnpPYl0Tjn5TjnC_6~lg4lHDJOrYV9zAXiXKl"
api_uid
"Cmy3GmRy2c9HZwB7rb4BAg=="
currency
"USD"
dilx
"Olpu1R6JAoW6OApDTrBYF"
goods
"goods_8smjeu"
hfsc
"L32CfYs04Tr+1JLOfg=="
language
"en"
njrpl
"sy4fOPlsBJrzI3FlGEWbyu7elgTBZapa"
region
"211"
shipping_city
"211,211000000025949"
timezone
"America/Chicago"
webp
"1"

{'Server': 'Nginx', 'Date': 'Tue, 30 May 2023 02:46:33 GMT', 'Content-Type': 'text/html; charset=UTF-8',
 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Vary': 'Accept-Encoding, User-Agent',
 'Content-Language': 'en', 'Surrogate-Control': 'no-store',
 'Cache-Control': 'no-cache, must-revalidate, proxy-revalidate, max-age=0', 'Pragma': 'no-cache', 'Expires': '0',
 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff',
 'Set-Cookie': 'AccessToken=; Domain=.temu.com; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
 'X-Accel-Buffering': 'no', 'Content-Encoding': 'gzip',
 'x-yak-request-id': '1685414793820-a955b1ac7c6b0b2dabd02c15153a2690', 'strict-transport-security': 'max-age=2592000',
 'Content-Security-Policy-Report-Only': "default-src *.temu.com *.kwcdn.com  wss://*.temu.com  *.googleapis.com *.gstatic.com *.googletagmanager.com *.google-analytics.com *.analytics.google.com *.doubleclick.net *.google.com *.googlesyndication.com *.googleusercontent.com www.googleadservices.com www.google.cn www.google.com.hk www.google.co.uk www.google.ca  www.google.com.au www.google.co.nz google.com connect.facebook.net www.facebook.com appleid.cdn-apple.com socialplugin.facebook.net *.cash.app *.forter.com blob: data: 'unsafe-eval' 'unsafe-inline' 'wasm-eval'; report-uri /api/sec-csp/c/sec-gif",
 'x-frame-options': 'SAMEORIGIN', 'cip': '136.22.18.140'}
