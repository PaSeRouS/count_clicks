import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


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


def main():
    load_dotenv()
    
    token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    url = args.url

    parse = urlparse(url)
    checked_url = '{netloc}{path}'.format(netloc=parse.netloc, path=parse.path)

    try:
        if is_bitlink(token, checked_url):
            print('Количество кликов:', count_clicks(token, checked_url))
        else:
            print('Битлинк:', shorten_link(token, url))
    except requests.exceptions.HTTPError:
        print("Ошибка! Неправильная ссылка!")


if __name__ == "__main__":
    main()
