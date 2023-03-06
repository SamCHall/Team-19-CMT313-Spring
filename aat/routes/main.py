from flask import render_template

from ..aat import app

@app.route("/")
def home():
    return render_template('home.html', title='Home')
