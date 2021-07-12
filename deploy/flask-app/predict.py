import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from tensorflow import keras

from .preprocessing import preprocess_input

import pandas as pd

bp = Blueprint('auth', __name__, url_prefix='/predict')

@bp.route('', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        #return str(request.form)
        title = request.form['poem-title']
        text = request.form['poem-text']
        error = None

        print(title)

        print(text[:50])

        df_input = pd.DataFrame([[title, text]], columns=['title', 'text'])

        print(df_input)

        df_preproc = preprocess_input(df_input)

        #print(predict(df_preproc))

        predictions =  predict(df_preproc)

        if len(title + text) < 150:
            error = 'The text is too short.'

        if error is None:
            #here we use our models to predict
            return render_template('prediction_result.html', prediction_num=predictions)

        flash(error)

    return render_template('predict.html')


def load_models():
    themes_to_predict = ['nature', 'family', 'love', 'body', 'animals']
    
    bin_models = {}
    for theme in themes_to_predict:
        bin_models['model_' + theme] = keras.models.load_model('baby_models/model_' + theme + '.h5')
        
    return bin_models


def predict(df_input_prp):
    themes_to_predict = ['nature', 'family', 'love', 'body', 'animals']
    bin_models = load_models()
    
    models_predictions = {}
    for theme in themes_to_predict:
        bin_mod = bin_models['model_' + theme]

        predictions = bin_mod.predict(df_input_prp)
        models_predictions['model_' + theme] = predictions
        
    return models_predictions