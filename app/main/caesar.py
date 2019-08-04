import requests
import json
import re
import string
import random
import re
import os

quotes_path = os.path.join('app', 'main', 'config/indexed_quotes.json')

with open(quotes_path, 'r') as f:
    quotes = json.load(f)


def get_random_text(level="hard"):
    """
    Get quotes from config -
    level is easy, medium, or hard
    """
    #choose a key
    selection = ''.join(random.sample( quotes.get(level).keys(), 1))
    quote = quotes[level][selection]
    quote =  re.sub(r'([^\s\w]|_)+', '', quote)
    return { "index": selection,
             "content" : quote}


def caesar(plaintext, shift):
    """
    Shift string by a {shift} amount
    """
    alphabet = string.ascii_lowercase
    split_message = plaintext.lower().split(' ')
    output = []

    for message_part in split_message:
        indices = [(alphabet.index(c) + shift) % len(alphabet) \
                   for c in message_part \
                   if c in alphabet]
        encrypted_part = ''.join([alphabet[i] for i in indices])
        output.append(encrypted_part)

    return (' '.join(output))


def make_caesar_challenge(number_of_problems, level="easy"):
    problems = []
    
    # To be safe, max out at 200
    if number_of_problems > 20:
        number_of_problems = 20
    for i in range(number_of_problems):
        quote = get_random_text(level)
        cleartext = quote['content']
        shift = random.randint(1, 25)
        ciphertext = caesar(cleartext, shift)

        problems.append({
            "number": quote['index'],
            "cleartext": cleartext.split(),
            "ciphertext": ciphertext.split(),
            "shift": shift
        })

    return problems


def random_substution(plaintext):
    alphabet = string.ascii_lowercase
    new_alphabet = ''.join(random.sample(alphabet, len(alphabet)))
    trantab = string.maketrans(alphabet, new_alphabet)
    return str(plaintext).translate(trantab)


def make_rs_challenge(number_of_problems, level="easy"):
    problems = []
    for i in range(number_of_problems):
        quote = get_random_text(level)
        cleartext = quote['content']
        ciphertext = random_substution(cleartext)
        problems.append({
            "number": quote['index'],
            "cleartext": cleartext.split(),
            "ciphertext": ciphertext.split(),
        })
    return problems


if __name__ == "__main__":
    shift = random.randint(1, 25)
    print(shift)
    print(caesar("this is some string", shift))
    guess = int(input("Guess the shift:"))
    while guess != shift:
        guess = int(input("Nah fam, guess again\n"))
    print("Congratulations!")
