import os
import base64
import logging
import traceback

from io import BytesIO
from utils import get_original_link
from capture import capture
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html', result='', image=None, error=None)

@app.route('/search', methods=['POST'])
def search():
    url = request.form['url']
    try:
        original_url = get_original_link(url)
        image = capture(original_url)
        buf = BytesIO()
        image.save(buf, format='png')
        image_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        error = None
        result = original_url
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        image_str = None
        error = str(e)
        result = None

    return render_template('index.html', error=error, result=result, image=image_str)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
