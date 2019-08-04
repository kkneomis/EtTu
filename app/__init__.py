
# Importing flask functions to be used 
from flask import Flask, render_template, redirect\
, url_for, flash, request, session, send_file

#local imports
from caesar import *

#just for me :)
import json
import string
import os
import StringIO 
import requests
import random
from werkzeug import secure_filename

# Instantiating the flask Object
application = Flask(__name__)

#I'm lazy and want to use an abreviation
app = application


app.config['UPLOAD_FOLDER'] = '/tmp/'
app.config.from_object(os.environ['APP_SETTINGS'])
#app.config.from_object('module_name.DevelopmentConfig')
#app.config.from_envvar('APP_SETTINGS')

config = {}
indexed_quotes = {}

@app.route('/')
def home():
    """
    Render the main page
	Request goes to process input
    """
    return render_template("index.html")


@app.route('/solve_menu')
def solve_menu():
    """
    Render the page to choose a specific problem to solver
    """
    return render_template("solve_menu.html")

@app.route('/guess_menu')
def guess_menu():
    """
    Render the page to choose a specific problem to solver
    """
    return render_template("guess_menu.html")



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

	elif challenge_type == 2:
		challenges = make_rs_challenge(number_of_problems, level=level)
		questions = render_template('pdf/problems.txt', 
									challenges=challenges,
									cipher_type = "Random Substitution")
		answers = render_template('pdf/answers.txt', 
									challenges=challenges,
									cipher_type = "Random Substitution")


	config['questions'] = questions
	config['answers'] = answers
	return redirect(url_for('download'))

@app.route('/download')
def download():
	questions = config.get('questions', "None")
	answers = config.get('answers', "None")
	
	questions_link = url_for('return_files', data=questions)
	answers_link = url_for('return_files', data=answers)

	return render_template('download.html',
							questions_link=questions_link,
							answers_link=answers_link)


@app.route('/return-files/', methods=['GET', 'POST'])
def return_files():
    #Temporary dowload link for generated files
	data = request.args.get("data")
	filename = os.path.join(app.config['UPLOAD_FOLDER'], "ettuproblems.txt")
	#os.remove(filename)
	with open(filename, 'w') as file:
		file.write(data)
	try:
		return send_file(filename)
	except Exception as e:
		return str(e)

@app.route('/solve_problem')
def solve_problem():
    """
    Render the solve page
	Request goes to solve_problem
    """
    return render_template("solve_main.html")

@app.route('/solve')
@app.route('/solve?challenge_type=<challenge_type>&difficulty=<level>&id=<id>', methods=['GET'])
def solve(level="easy", id="-1", challenge_type="rot" ):
    """Solve a problem by id"""
    
    level =  request.args.get('level', 'easy')
    id = request.args.get('id', -1)
    challenge_type = request.args.get('challenge_type', 'rot')
    
    
    if not indexed_quotes:
        load_indexed_quotes()
        print "------- Got the quotes ---------"
    
    if (not id) or (int(id) < 0):
        print int(id)
        quote = get_random_text(level)['content']
        print "Getting random challenge"
    else:
        quote = indexed_quotes[level].get(str(id), "None").lower()
        
    if not quote:
        return "No such puzzle"
    
    
    ciphertext = "No such puzzle"
    #Create the problem based on the type
    if challenge_type == 'rot':
        ciphertext = caesar(quote, random.randint(1,26))
    elif challenge_type == 'sub':
        ciphertext =  random_substution(quote)

           
    # Cleartext and ciphertext to be parsed in the view
    text= {}
    text['ciphertext'] = ciphertext.split()
    text['cleartext'] = quote.split()
    
    # Data for the letter frequency charts
    alphabet = string.ascii_lowercase
    cipher_text_freq =  get_letter_frequencies(ciphertext)['values']
    cipher_text_keys = json.dumps(get_letter_frequencies(ciphertext)['keys'])
    return render_template("solve.html", 
    						text=text,
    						alphabet=alphabet, 
                            challenge_type = challenge_type,
    						cipher_text_freq = cipher_text_freq,
    						cipher_text_keys = cipher_text_keys)



	
def get_letter_frequencies(phrase):
    # the ciphertext is broken into a list. Convert back to string
    if isinstance(phrase, list):
        phrase = ' '.join(phrase)
 
    alphabet = string.ascii_lowercase
    freq = {}
    for letter in alphabet:
        freq[letter] = round(phrase.count(letter)/float(len(phrase)),10)

    return { "keys":sorted(freq, key=freq.get, reverse=True),
	         "values": sorted(freq.values(), reverse=True) }
	

    
def load_indexed_quotes():
    """This is inefficient, but I'm lazy...so fck it"""
    with open('config/indexed_quotes.json', 'r') as f:
        quotes = json.load(f)
    indexed_quotes['easy'] = quotes['easy']
    indexed_quotes['medium'] = quotes['medium']
    indexed_quotes['hard'] = quotes['hard']

    

@app.route('/guess')
@app.route('/guess?challenge_type=<challenge_type>&difficulty=<level>&id=<id>', methods=['GET'])
def guess(level="easy", id="-1", type="rot"):
    """
    Return  cipher text
    rot or sub
    """
    
    level =  request.args.get('level', 'easy')
    id = request.args.get('id', -1)
    challenge_type = request.args.get('challenge_type', 'rot')
    
    if not indexed_quotes:
        load_indexed_quotes()
        print "------- Got the quotes ---------"
                
    if level not in ['easy', 'medium', 'hard']:
        return "No such puzzle"
    
    
    if int(id) < 0:
        print int(id)
        quote = get_random_text(level)['content']
        print "Getting random challenge"
    else:
        quote = indexed_quotes[level].get(str(id), "None").lower()
        
    if not quote:
        return "No such puzzle"
    
    
    if type == 'rot':
        problem = caesar(quote, random.randint(1,26))
    elif type == 'sub':
        problem =  random_substution(quote)
    else:
        problem = "No such puzzle"
        answer = ""
    
    
    return render_template( "check_answer.html",
                            problem =  problem,
                            answer = quote )


@app.route('/shift_alphabet', methods=['GET', 'POST'])
def shift_alphabet():
    shift = int(request.form['shift'])
    alphabet = string.ascii_lowercase
    try:
        return caesar(alphabet, shift)
    except:
        return "Error"
     



if __name__ == "__main__":   
    app.run(debug=app.config['DEBUG'])
    
