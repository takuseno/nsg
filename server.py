import os
import base64

from io import BytesIO
from utils import get_original_link
from capture import capture
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', result='', image=None)

@app.route('/search', methods=['POST'])
def search():
    url = request.form['url']
    try:
        result = get_original_link(url)
        image = capture(result)
        buf = BytesIO()
        image.save(buf, format='png')
        image_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception as e:
        image_str = None
        result = str(e)
    return render_template('index.html', result=result, image=image_str)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
