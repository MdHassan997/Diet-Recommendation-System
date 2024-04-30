from flask import Flask, render_template, request , send_from_directory
import os
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dietplan')
def diet():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def mealplan():
    if request.method == 'POST':
        # Access form data
        diet_type = request.form.get('diet')
        disease = request.form.get('disease')
        veg_non_veg = request.form.get('veg_non_veg')
        nutrient = request.form.get('nutrient')
        
        # Process form data as needed
        # For example, you can pass the form data to the results template
        return render_template('results.html', diet=diet_type, disease=disease, veg_non_veg=veg_non_veg, nutrient=nutrient)
    else:
        # Handle GET requests to /result route if needed
        return render_template('error.html', message='Method Not Allowed')



if __name__ == "__main__":
    app.run(debug=True, port=8000)
    