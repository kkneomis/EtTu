
# Importing flask functions to be used 
from flask import Flask, render_template, redirect\
, url_for, flash, request, session, send_file

#local imports
from caesar import make_caesar_challenge, make_rs_challenge 

#just for me :)
import json
import string
import os
import StringIO 
from werkzeug import secure_filename

# Instantiating the flask Object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'

@app.route('/')
def home():
    """
    Render the main page
	Request goes to process input
    """
    return render_template("index.html")

@app.route('/processinput', methods=['GET', 'POST'])
def processinput():
	"""
	Create a challenge set based on specification
	Use can get these files on the download page
	"""
	challenge_type =  int(request.form['challenge_type'])
	number_of_problems = int(request.form['number_of_problems'])
	level = request.form['difficulty']


	if challenge_type == 1:
		challenges = make_caesar_challenge(number_of_problems, level=level)
		#print json.dumps(challenges, indent=4)
		questions = render_template('pdf/problems.txt', 
									challenges=challenges,
									cipher_type = "Caesar Cipher")
		answers = render_template('pdf/answers.txt', 
									challenges=challenges,
									cipher_type = "Caesar Cipher")

		return redirect(url_for('download', 
								questions=questions, answers= answers))
	elif challenge_type == 2:
		challenges = make_rs_challenge(number_of_problems, level=level)
		questions = render_template('pdf/problems.txt', 
									challenges=challenges,
									cipher_type = "Random Substitution")
		answers = render_template('pdf/answers.txt', 
									challenges=challenges,
									cipher_type = "Random Substitution")

	return redirect(url_for('download', 
							questions=questions, 
							answers= answers))


@app.route('/return-files/', methods=['GET', 'POST'])
def return_files():
	data = request.args.get("data")
	filename = os.path.join(app.config['UPLOAD_FOLDER'], "ettuproblems.txt")
	#os.remove(filename)
	print data
	with open(filename, 'w') as file:
		file.write(data)
	try:
		return send_file(filename)
	except Exception as e:
		return str(e)

@app.route('/download')
def download():
	questions = request.args.get("questions")
	answers = request.args.get("answers")
	questions_link = url_for('return_files', data=questions)
	answers_link = url_for('return_files', data=answers)

	return render_template('download.html',
							questions_link=questions_link,
							answers_link=answers_link)

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




	
def get_letter_frequencies(phrase):
	alphabet = string.ascii_lowercase
	freq = {}
	for letter in alphabet:
		freq[letter] = round(phrase.count(letter)/float(len(phrase)),10)

	return { "keys":sorted(freq, key=freq.get, reverse=True),
	         "values": sorted(freq.values(), reverse=True) }
	


if __name__ == "__main__":   
	app.run(debug=True)