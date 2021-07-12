import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow import keras
from utils import convert_to_decade, preprocess_input, themes_prediction
import pickle

app = Flask(__name__)
model1 = keras.models.load_model('year_prediction.h5')
with open('tokenizer1.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    form = ''
    for x in request.form.values():
        form.join(x)
    input = preprocess_input(form, tokenizer)
    prediction = model1.predict(input)
    output1 = convert_to_decade(prediction[0][0])
    output2 = ', '.join(themes_prediction(form, tokenizer))

    return render_template('index.html', prediction_text1=f"""This poem was written in {output1}""", prediction_text2 =f"The themes are: {output2}")


if __name__ == "__main__":
    app.run(debug=True)