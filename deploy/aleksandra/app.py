import json

import numpy as np
from flask import Flask, request, jsonify, render_template
from keras_preprocessing.text import tokenizer_from_json
from tensorflow import keras
from utils import convert_to_decade, preprocess_input, themes_prediction
import pickle

app = Flask(__name__)
model1 = keras.models.load_model('year_prediction.h5')
with open('tokenizer1.pickle', 'rb') as handle:
    tokenizer1 = pickle.load(handle)
with open('tokenizer2.json') as handle2:
    data = json.load(handle2)
    tokenizer2 = tokenizer_from_json(data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    title = request.form['title']
    text = request.form['text']
    form = title + ' ' + text
    input = preprocess_input(form, tokenizer1)
    prediction = model1.predict(input)
    output1 = convert_to_decade(prediction[0][0])
    output2 = ', '.join(themes_prediction(form, tokenizer2))

    return render_template('index.html', prediction_text1=f"""This poem was written in {int(output1)}s""", prediction_text2 =f"The themes are: {output2}")


if __name__ == "__main__":
    app.run(debug=True)