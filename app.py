
# Importing flask functions to be used 
from flask import Flask, render_template, redirect, url_for, flash, request, session

#local imports
from caesar import make_caesar_challenge, make_rs_challenge 

#just for me :)
import json
import string

# Instantiating the flask Object
app = Flask(__name__)

@app.route('/')
def home():
    """Render the main page"""
    return render_template("index.html")


@app.route('/solve')
def solve():
    """Render the main page"""
    text =  make_caesar_challenge(1)[0]
    
    alphabet = string.ascii_lowercase

    cipher_text_freq =  get_letter_frequencies(text['ciphertext'])['values']
    cipher_text_keys = json.dumps(get_letter_frequencies(text['ciphertext'])['keys'])
    return render_template("solve.html", 
    						text=text,
    						alphabet=alphabet, 
    						cipher_text_freq = cipher_text_freq,
    						cipher_text_keys = cipher_text_keys)


@app.route('/processinput', methods=['GET', 'POST'])
def processinput():
	challenge_type =  int(request.form['challenge_type'])
	text_length = int(request.form['text_length'])
	number_of_problems = int(request.form['number_of_problems'])

	if challenge_type == 1:
		challenges = make_caesar_challenge(number_of_problems)
		#print json.dumps(challenges, indent=4)
		return render_template('pdf/answers.html', challenges=challenges)
	elif challenge_type == 2:
		challenges = make_rs_challenge(number_of_problems)
		#print json.dumps(challenges, indent=4)
		return render_template('pdf/answers.html', challenges=challenges)
	else:
		return redirect(url_for('home'))

	
def get_letter_frequencies(phrase):
	alphabet = string.ascii_lowercase
	freq = {}
	for letter in alphabet:
		freq[letter] = round(phrase.count(letter)/float(len(phrase)),10)
	

	return { "keys":sorted(freq, key=freq.get, reverse=True),
	         "values": sorted(freq.values(), reverse=True) }
	



if __name__ == "__main__":   
	app.run(debug=True)