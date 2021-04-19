import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter
import io


BASE_URL = 'http://quotes.toscrape.com'


def scrape_quotes():
    url = '/page/1'
    all_quotes = []
    while url:
        data = requests.get(f'{BASE_URL}{url}')
        # print(f'Now Scrapping this: {BASE_URL}{url}')
        soup = BeautifulSoup(data.text, 'html.parser')
        quotes = soup.find_all(class_='quote')
        for quote in quotes:
            all_quotes.append({
                'text': quote.find(class_='text').get_text(),
                'author': quote.find(class_='author').get_text(),
                'bio_link': quote.find('a')['href']
            })
        # sleep(2)
        next_btn = soup.find(class_='next')
        url = next_btn.find('a')['href'] if next_btn else None
    return all_quotes


def write_quotes(quotes):
    quotes = scrape_quotes()
    with io.open('quotes.csv', "w", encoding='utf-16') as file:
        headers = ['text', 'author', 'bio_link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)