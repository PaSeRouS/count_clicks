import argparse
import os
import requests

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {"long_url": url}

    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=data
    )
    response.raise_for_status()

    return response.json()['id']


def count_clicks(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'unit': 'day',
        'units': '-1'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=headers,
        params=params
    )
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=headers
    )

    return response.ok


if __name__ == "__main__":
    load_dotenv()
    
    TOKEN = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    url = args.url

    parse = urlparse(url)
    checked_url = '{netloc}{path}'.format(netloc=parse.netloc, path=parse.path)

    try:
        if is_bitlink(TOKEN, checked_url):
            print('Количество кликов:', count_clicks(TOKEN, checked_url))
        else:
            print('Битлинк:', shorten_link(TOKEN, url))
    except requests.exceptions.HTTPError:
        print("Ошибка! Неправильная ссылка!")
