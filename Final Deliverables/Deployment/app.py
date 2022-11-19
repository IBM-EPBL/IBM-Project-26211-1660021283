from flask import Flask, render_template, request
from flask_cors import CORS
import joblib
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Ajx7BZ64A-kNZlcGlAyn4Dr-RYfooJomuf0V44dWXDDZ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction_form')
def predict1():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = float(request.form['Age']) 
    gender = float(request.form['Gender'])
    tb = float(request.form['Total_Bilirubin']) 
    db = float(request.form['Direct_Bilirubin'])
    ap = float(request.form['Alkaline_phosphatase'])
    aa1 = float(request.form['Alamine_Aminotransferase'])
    aa2 = float(request.form['Aspartate_Aminotranferase'])
    tp = float(request.form['Total_Proteins'])
    al = float(request.form['Albumin'])
    agr = float(request.form['Albumin_and_Globulin_Ratio'])

    # converting data into float
    X = [[age,gender,tb,db,ap,aa1,aa2,tp,al,agr]]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [['age','gender','tb','db','ap','aa1','aa2','tp','al','agr']], "values": X }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/06acb9ea-228d-4770-8841-afb3a9cedc6c/predictions?version=2022-11-16', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring.json())
    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print(f"Final prediction : {predict}")
    # prediction = model.predict(data)[0]

    return render_template('result.html',result = predict)

if __name__ == '__main__':
    app.run(debug=True)


# SVC from version 1.0.2 when using version 1.1.3.


# 2 - have disease      - 1
# 1 - Not have disease  - 0

    
