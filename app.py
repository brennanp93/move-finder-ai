import os

import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "tuna"
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET","POST"))
def index():
    if request.method == "POST":
        description = request.form["description"].capitalize()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(description),
            temperature=0.7,            
        )
        # session['input'] = description
       

        return redirect(url_for("index", result=response.choices[0].text, input=description))
    result = request.args.get("result")
    input = request.args.get("input")
    session['user_input'] = input
    session['output'] = result
    return render_template("index.html", result=result, input=input )


@app.route('/share/twitter')
def share_twitter():
    user_input=session['user_input']
    output=session['output'].lstrip()
    url='https://movie-finder-ai.herokuapp.com/'
    text=f'Amazing! I described a movie as:\n"{user_input}" \nand the AI correctly guessed it was:\n{output} \nCan you challenge its movie guessing skills?\nTry it now at'
    tweet_url=f'https://twitter.com/intent/tweet?url={url}&text={text}'
    return redirect(tweet_url)

def generate_prompt(movie_description):
    return """Help me find out the name of a movie based on a brief description. 

Description: Movie where Leonardo Dicaprio plays a con artist.
Movie: Catch Me If You Can. Released in 2002.
Description: Movie where Simon Pegg fights zombies with his friend.
Movie: Shaun of the Dead. Realsed in 2004.
Description: Movie where a weird guy takes over a tv station in the 80's.
Movie: UHF. Released in 1989.
Description: Jean reno and Jon Voight are bad guys.
Movie: Mission: Impossible. Released in 1996.
Description: {}
Movie:""".format(movie_description.capitalize())

