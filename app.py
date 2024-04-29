from flask import Flask, render_template, send_from_directory
import os
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dietplan')
def diet():
    return render_template('home.html')

@app.route('/results')
def mealplan():
    return render_template('results.html')



if __name__ == "__main__":
    app.run(debug=True, port=8000)
    