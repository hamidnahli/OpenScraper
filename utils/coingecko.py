import os

import requests
import urllib.parse

from dotenv import load_dotenv

load_dotenv()


def make_request(r_url):
    token = os.getenv('PROXY_API')
    targetUrl = urllib.parse.quote(r_url)
    r_url = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", r_url)
    return response


def get_social_links(container):
    if container:
        container = container[0]
        div = container.div
        links = div.findAll('a')
        twitter = [l['href'] for l in links if 'twitter.com' in l['href']]
        telegram = [l['href'] for l in links if 't.me' in l['href']]
        discord = [l['href'] for l in links if 'discord.gg' in l['href']]
        return twitter[0] if twitter else None, telegram[0] if telegram else None, discord[0] if discord else None
    return None, None, None


def get_block_explorers(container):
    if container:
        container = container[0]
        explorers = container.findAll('a')
        explorers = [a['href'] for a in explorers if a.get('href')]
        return explorers
    return None


def get_websites(container):
    if container:
        container = container[0]
        websites = container.findAll('a')
        websites = [a['href'] for a in websites if a.get('href')]
        return websites
    return None


def get_contracts(container):
    if container:
        container = container[0]
        contracts = container.findAll('i')
        contracts = [c['data-address'] for c in contracts]
        return contracts
    return container
