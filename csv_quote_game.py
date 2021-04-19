import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader


BASE_URL = 'http://quotes.toscrape.com'


def read_quotes(filename):
    with open(filename, 'r', encoding='utf-16') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def play_game(quotes_data):
    quote = choice(quotes_data)
    remaining_guesses = 4
    print('Here\'s a quote for you:')
    print(quote['text'])
    guess = ''

    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        guess = input(f'Who said this quote? Guesses remaining {remaining_guesses}. Your answer: ')
        if guess.lower() == quote['author'].lower():
            print("You're right!")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{quote['bio_link']}")
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_='author-born-date').get_text()
            birth_location = soup.find(class_='author-born-location').get_text()
            print(f"Here's a hint, author was born on {birth_date}")
            print(f"{birth_location}")
        elif remaining_guesses == 2:
            print(f'First name starts with: {quote["author"][0]}')
        elif remaining_guesses == 1:
            print(f'Last name initial starts with: {quote["author"].split(" ")[1][0]}')
        else:
            print('You run out of guesses')
            print(f'The answer was {quote["author"]}')
    again = ''
    while again not in ('yes', 'no', 'y', 'n'):
        again = input('Would you like to play again?(y/n)')
        if again.lower() in ('yes', 'y'):
            return play_game(quotes_data)
        else:
            return print('Good bye')


quotes_data = read_quotes('quotes.csv')
play_game(quotes_data)
