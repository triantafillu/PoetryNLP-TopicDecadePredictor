import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/predict')

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
            return render_template('prediction_result.html')

        flash(error)

    return render_template('predict.html')
