import requests
import json
import re
import string
import random
from bs4 import BeautifulSoup


def get_random_text():
	r = requests.get('http://www.randomtext.me/api/gibberish/p-1/25-45')
	res = r.json()['text_out']

	soup = BeautifulSoup(res, 'lxml')
	clear_text =  soup.text

	return clear_text


def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)


sample_text = str(get_random_text())
shift = random.randint(1,25)
print caesar(sample_text, shift)
print "shift, is", shift
guess = int(raw_input("Guess the shift:"))
while guess != shift:
	guess = int(raw_input("Nah fam, guess again"))
print "Congratulations!"
