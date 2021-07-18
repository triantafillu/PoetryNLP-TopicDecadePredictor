import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import json
import requests
from tensorflow import keras

from .preprocessing import preprocess_input

import numpy as np
import pandas as pd

bp = Blueprint('auth', __name__, url_prefix='/predict')

THEMES_TO_PREDICT = ['nature', 'family', 'love', 'body', 'animals', 'arts & sciences', 'religion', 'death', 'war', 'heartache']

@bp.route('', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        #return str(request.form)
        title = request.form['poem-title']
        text = request.form['poem-text']
        error = None
      

        if len(title + text) < 150:
            error = 'The text is too short.'

        if error is None:
            #here we use our models to predict
            predictions = {}
            df_input = pd.DataFrame([[title, text]], columns=['title', 'text'])
            df_preproc = preprocess_input(df_input)
            
            df_preproc = np.reshape(df_preproc, (1,150))
            predictions = predict_categories_served(df_preproc)
            
            return render_template('prediction_result.html', predictions=predictions)

        flash(error)

    return render_template('predict.html')


def load_models():
    
    bin_models = {}
    for theme in THEMES_TO_PREDICT:
        bin_models['model_' + theme] = keras.models.load_model('flask-app/baby_models/model_' + theme + '.h5')
        
    return bin_models


def predict_categories(df_input_prp):
    bin_models = load_models()
    
    models_predictions = {}
    for theme in THEMES_TO_PREDICT:
        bin_mod = bin_models['model_' + theme]

        predictions = bin_mod.predict(df_input_prp)
        models_predictions['model_' + theme] = predictions[0][0]
        
    return models_predictions
    

def predict_categories_served(df_input_prp):    
    df_input_prp = df_input_prp.tolist()
    
    payload2 = json.dumps({"instances": df_input_prp})
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    themes_predictions = {}
    models_predictions = {}
    for theme in THEMES_TO_PREDICT:
        r = requests.post('http://localhost:8501/v1/models/model_{}:predict'.format(theme), data=payload2, headers=headers)
        themes_predictions[theme] = r.json()['predictions'][0][0]
    r = requests.post('http://localhost:8501/v1/models/year_model:predict', data=payload2, headers=headers)
    
    models_predictions['themes'] = themes_predictions
    models_predictions['year'] = int(r.json()['predictions'][0][0])
    return models_predictions

    
def predict_year(df_input_prp):
    year_prediction_model = keras.models.load_model('flask-app/year_prediction_model.h5', compile=False)
    year_prediction = round(year_prediction_model.predict([df_input_prp])[0][0])
        
    return year_prediction
