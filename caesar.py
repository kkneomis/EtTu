import requests
import json
import re
import string
import random
from bs4 import BeautifulSoup



with open('config/quotes.txt', 'r') as f:
	quotes = json.load(f)


def get_random_text(level="hard"):
	'''
	Get quotes from config
	level is easy, med, or hard
	'''
	# we haven't initialized it yet
	quote = random.choice(quotes[level])
	return quote


def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    split_message = plaintext.lower().split(' ')
    output = []

    for message_part in split_message:
        indices = [(alphabet.index(c) + shift) % len(alphabet) \
                   for c in message_part\
                   if c in alphabet]
        encrypted_part = ''.join([alphabet[i] for i in indices])
        output.append(encrypted_part)

    return (' '.join(output))

def make_caesar_challenge(number_of_problems, level="easy"):
	problems = []
	for i in range(number_of_problems):
		cleartext = get_random_text(level)
		print cleartext
		shift = random.randint(1,25)
		ciphertext = caesar(cleartext, shift)

		problems.append({
				"cleartext":cleartext,
				"ciphertext":ciphertext,
				"shift": shift
			})

	return problems

def random_substution(plaintext):
    alphabet = string.ascii_lowercase
    new_alphabet = ''.join(random.sample(alphabet,len(alphabet)))
    trantab = string.maketrans(alphabet, new_alphabet)
    return plaintext.translate(trantab)


def make_rs_challenge(number_of_problems, level="easy"):
	problems = []
	for i in range(number_of_problems):
		cleartext = get_random_text(level)
		ciphertext = random_substution(str(cleartext))
		problems.append({
				"cleartext":cleartext,
				"ciphertext":ciphertext,
			})
	return problems


if __name__ == "__main__":
	shift = random.randint(1,25)
	print caesar( shift)
	print "shift, is", shift
	guess = int(raw_input("Guess the shift:"))
	while guess != shift:
		guess = int(raw_input("Nah fam, guess again"))
	print "Congratulations!"
