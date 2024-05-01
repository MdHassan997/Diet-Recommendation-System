from flask import Flask, render_template, request , send_from_directory, jsonify, json, session
import os
import pandas as pd

app=Flask(__name__,static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key'

dataset = pd.read_csv('templates/calories.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dietplan')
def diet():
    return render_template('home.html')

# @app.route('/result', methods=['POST'])
# def mealplan():
#     if request.method == 'POST':
#         # Access form data
#         diet_type = request.form.get('diet')
#         disease = request.form.get('disease')
#         veg_non_veg = request.form.get('veg_non_veg')
#         nutrient = request.form.get('nutrient')
        
#         # Process form data as needed
#         # For example, you can pass the form data to the results template
#         return render_template('results.html', diet=diet_type, disease=disease, veg_non_veg=veg_non_veg, nutrient=nutrient)
#     else:
#         # Handle GET requests to /result route if needed
#         return render_template('error.html', message='Method Not Allowed')
    
@app.route('/bmrForm',methods=["POST","GET"])
def bmrCalculate():
    return render_template('bmrForm.html')

@app.route('/bmiCalorieCalculate',methods=["POST","GET"])
def bmrCaloriecalculate():
    age=float(request.args.get('age'))
    height=float(request.args.get('height'))
    gender=request.args.get('gender')
    weight=float(request.args.get('weight'))
    Lifestyle=request.args.get('lifestyle')
    calorie = None
    if(gender=='male'):
        BMR=88.362+(13.397*weight)+(4.799*height)-(5.677*age)
    else:
        BMR = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age )

    if Lifestyle == "sedentary":
            calorie = int(BMR * 1.2)
    elif Lifestyle == "lightly_active":
            calorie = int(BMR * 1.375)
    elif Lifestyle == "moderately_active":
            calorie = int(BMR * 1.55)
    elif Lifestyle == "very_active":
            calorie = int(BMR * 1.725)
    elif Lifestyle == "extra_active":
            calorie = int(BMR * 1.9)
    
    # calorie = session.get('calorie_value')
    session['calorie'] = calorie

    return render_template('CaloriePage.html',BMR=BMR,calorie=calorie,Lifestyle=Lifestyle,)  

@app.route('/add-items')
def addItems():
    #    calorie=request.args.get('calorie')
    calorie = session.get('calorie')
    food_categories = dataset['FoodCategory'].unique()
    # foodItems = dataset.loc[dataset['FoodCategory'] == food_categories, 'FoodItems'].unique()
    # session['food_categories'] = food_categories

    return render_template('test.html',calorie=calorie,dataset=dataset,food_categories=food_categories)



# testing the code
@app.route("/test",methods=["POST","GET"])
def test():
    calorie = session.get('calorie')
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    return render_template('test.html',data=data,calorie= calorie)



@app.route('/data',methods=["POST","GET"])
def get_data():
    with open('static/data.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
    