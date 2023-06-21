from flask import Flask, render_template, request
import wikipedia
import random
import pycountry

app = Flask(__name__)

# list of random countries
countries = []
for country in pycountry.countries:
    if hasattr(country, "official_name"):
        if any(not c.isalnum() for c in country.name):
            countries.append(country.name)

# choose a random country
randomCountry = random.choice(countries)
page = wikipedia.page(randomCountry)
title = page.title
sentences = page.content.split(". ")
givenSentences = []
guesses = 5
points = 0

def play_game():
    global guesses, points, givenSentences
    answer = request.form.get("answer")
    if answer:
        if answer.lower() == title.lower():
            points += guesses*2
            result = ("You guessed correctly! +%i points!" % guesses*2)
        else:
            random_sentence = random.choice(sentences)
            givenSentences.append(random_sentence)
            result = ("Incorrect! Try again with another sentence:")
            guesses -= 1
    else:
        result = ("")
    if guesses == 0:
        result = ("Sorry, you're out of guesses! The answer was: " + title)
    return (title, givenSentences, result, points, guesses)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    global title, givenSentences, sentences, randomCountry, guesses, points
    if request.method == 'GET':
        return render_template('game.html', title=title, givenSentences=givenSentences, result="", points=points, guesses=guesses)
    elif request.method == 'POST':
        title, givenSentences, result, points, guesses = play_game()
        if guesses == 0 or (result == "You guessed correctly! +%i points!" % guesses*2):
            # Choose a new random country when the game is over
            randomCountry = random.choice(countries)
            page = wikipedia.page(randomCountry)
            title = page.title
            sentences = page.content.split(". ")
            givenSentences = []
            guesses = 5
            points = 0
        return render_template('game.html', title=title, givenSentences=givenSentences, result=result, points=points, guesses=guesses)

@app.route('/enter_name')
def enter_name():
    return render_template('enter_name.html')

@app.route('/category')
def category():
    return render_template('category.html')


if __name__ == '__main__':
    app.run(debug=True)
