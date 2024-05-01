# from flask import Flask, render_template, request , send_from_directory, jsonify, json, session
# from sklearn.neighbors import NearestNeighbors
# import os
# import pandas as pd
from flask import Flask,render_template,request, session, redirect, url_for,jsonify, redirect,json
import os
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler,LabelEncoder

app=Flask(__name__,static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key'

dataset = pd.read_csv('templates/calories.csv')
df = pd.read_csv('templates/food_data.csv')



@app.route('/')
def home():
    return render_template('index.html')



class Recommender:

    def __init__(self):
        self.df = pd.read_csv('templates/food_data.csv')

    def get_features(self):
        #getting dummies of dataset
        nutrient_dummies = self.df.Nutrient.str.get_dummies()
        disease_dummies = self.df.Disease.str.get_dummies(sep=' ')
        diet_dummies = self.df.Diet.str.get_dummies(sep=' ')
        veg_dummies = self.df.Veg_Non.str.get_dummies(sep=' ')
        feature_df = pd.concat([nutrient_dummies,disease_dummies,diet_dummies,veg_dummies],axis=1)

        return feature_df

    def k_neighbor(self,inputs):

        feature_df = self.get_features()

        #initializing model with k=20 neighbors
        model = NearestNeighbors(n_neighbors=7,algorithm='ball_tree')

        # fitting model with dataset features
        model.fit(feature_df)

        df_results = pd.DataFrame(columns=list(self.df.columns))


        # getting distance and indices for k nearest neighbor
        distnaces , indices = model.kneighbors(inputs)

        for i in list(indices):
            # df_results = df_results.append(self.df.loc[i])
            indices = list(indices.flatten())  # Flatten the indices array

            df_results = self.df.loc[indices] 

        df_results = df_results.filter(['Name','catagory','description'])
        df_results = df_results.drop_duplicates(subset=['Name'])
        df_results = df_results.reset_index(drop=True)

        def get_unique_values(self, column_name):
            return sorted(self.df[column_name].unique())
        return df_results


   

ob = Recommender()
data = ob.get_features()

total_features = data.columns
d = dict()
for i in total_features:
    d[i]=0
print(d)


@app.route('/food_rec',methods=['GET','POST'])
def food_rec():
 # unique_diet_types = sorted(ob.df['Diet'].unique())
    nutrient = sorted(df['Nutrient'].unique())
    return render_template('food_form.html',nutrient=nutrient)

@app.route('/results', methods=['GET', 'POST'])
def results():
    diet = request.args.get("diet")
    nutrient = request.args.get("nutrient")
    veg = request.args.get("veg")
    disease = request.args.get("disease")
    # selected_diet = request.args.get("diet")

    # Reset dictionary values
    for key in d:
        d[key] = 0

    # Set features based on input
    if diet:
        d[diet] = 1
    if nutrient:
        d[nutrient] = 1
    if veg:
        d[veg] = 1
    if disease:
        d[disease] = 1

    final_input = list(d.values())
    results = ob.k_neighbor([final_input])  # pass 2d array []
    return render_template("results.html", results=results)
    
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
    