
# Importing flask functions to be used 
from flask import Flask, render_template, redirect, url_for, flash, request, session

#local imports
from caesar import make_caesar_challenge, make_rs_challenge 

#just for me :)
import json

# Instantiating the flask Object
app = Flask(__name__)

@app.route('/')
def home():
    """Render the main page"""
    return render_template("index.html")


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

	

if __name__ == "__main__":   
	app.run(debug=True)