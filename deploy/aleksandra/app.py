import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow import keras
from utils import convert_to_decade, preprocess_input
import pickle

app = Flask(__name__)
model = keras.models.load_model('year_prediction.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

@app.route('/')
def home():
    return render_template('../Bootcamp-Repository-Language-2/deploy/aleksandra/templates/index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    form = ''
    for x in request.form.values():
        form.join(x)
    input = preprocess_input(form, tokenizer)
    prediction = model.predict(input)

    output = convert_to_decade(prediction[0])

    return render_template('../Bootcamp-Repository-Language-2/deploy/aleksandra/templates/index.html', prediction_text=f"""This poem was written in {int(output[0])}s\nThe themes are: """)


if __name__ == "__main__":
    app.run(debug=True)