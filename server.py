import os

from utils import get_original_link
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', result='')

@app.route('/search', methods=['POST'])
def search():
    url = request.form['url']
    try:
        message = get_original_link(url)
        return redirect(original_url)
    except Exception as e:
        message = e.message
    return render_template('index.html', result=message)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
