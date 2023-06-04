import json

from bs4 import BeautifulSoup

from utils.coingecko import *


def run_scraper() -> list:
    data = []
    for i in range(1, 2):
        url = f'https://www.coingecko.com/en/all-cryptocurrencies/show_more_coins?page={i}&per_page=300&'
        page = make_request(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        urls = soup.findAll('a')
        urls = ['https://www.coingecko.com' + u['href'] for u in urls]
        links = urls[:2]
        for url in links:
            try:
                page = make_request(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                containers = soup.findAll('div', {'class': 'coin-link-row tw-mb-0'})
                contracts_container = [c for c in containers if c.span and c.span.text.strip() == 'Contract']
                website_container = [c for c in containers if c.span and c.span.text.strip() == 'Website']
                explorers_container = [c for c in containers if c.span and c.span.text.strip() == 'Explorers']
                community_container = [c for c in containers if c.span and c.span.text.strip() == 'Community']

                name = soup.find('h1', {'class': 'tw-m-0 tw-text-base'}).span.text.strip()
                twitter, telegram, discord = get_social_links(community_container)
                block_explorer = get_block_explorers(explorers_container)
                item = {
                    'name': name,
                    'url': url,
                    # 'chain': chain,
                    'block_explorer': block_explorer,
                    'discord': discord,
                    'twitter': twitter,
                    'telegram': telegram,
                    'contract': get_contracts(contracts_container),
                    'website': get_websites(website_container)
                }
                data.append(item)
                # with open('coingecko.json', 'a') as f:
                #     f.write(json.dumps(item))
                #     f.write('\n')
                print(f'{i}:{urls.index(url)} - {item}')
            except:
                print(f'{i}:{urls.index(url)} - Failed')
    return data

