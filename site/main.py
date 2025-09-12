from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1>ugyfugyfgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggfffffffffff</h1>'

@app.route("/secret")
def secret():
    stri = ""
    for i in range(1000):
        x = random.random() * 100
        print(x)
        if x > (100 - 49.9917):
            stri += " решка "
        elif x < 49.9917:
            stri += " орёл "
        else:
            stri += " РЕБРО "
    return '<h2> ' + stri + ' </h2>'

app.run(debug=True)