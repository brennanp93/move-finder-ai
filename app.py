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
            temperature=0.8,            
        )
        session['input'] = description
       
        print(input)
        return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result,  input = session["input"])


def generate_prompt(movie_description):
    return """Help me find out the name of a movie based on a brief description. 

Description: Movie where Leonardo Dicaprio plays a con artist
Movie: Catch Me If You Can. Released in 2002
Description: Movie where Simon Pegg fights zombies with his friend.
Movie: Shaun of the Dead. Realsed in 2004
Description: {}
Movie:""".format(movie_description.capitalize())