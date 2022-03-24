from flask import Flask, render_template, request
import jsonify
import json
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('home_price', 'rb'))
with open("clms.json", "r") as f:
    data_columns = json.load(f)['data_columns']
    locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    if request.method == 'POST':
        location = (request.form['location'])
        try:
            loc_index = data_columns.index(location.lower())
        except:
            loc_index = -1
        sqft = float(request.form['sqft'])
        bath=int(request.form['bath'])
        bhk=int(request.form['bhk'])
        
    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    
        output=round(model.predict([x])[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this house")
        else:
            return render_template('index.html',prediction_text="You Can Sell The house at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)