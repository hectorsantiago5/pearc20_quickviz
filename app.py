import base64
import csv
import json
import os
import urllib
from urllib.request import urlretrieve as retrieve
from werkzeug.utils import secure_filename
import requests

from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to connect our home HTML file
@app.route('/')
def index():
    return render_template('index.html')


# Function to connect our about us HTML file
@app.route('/aboutus')
def about_us():
    return render_template('About.html')


# Function to get a COVID-19 data file and display the contents of it
@app.route('/covid')
def import_covid_csv():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    retrieve(url, 'covid_file/us.csv')


# Function to only allow CSV files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to redirect filename
@app.route('/upload')
def upload_file():
    return redirect(url_for('get_csv', filename=upload_file))


# Function to get a data file and display the contents of it
@app.route('/uploader', methods=['GET', 'POST'])
def get_csv():
    # try:
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Successful')
            return redirect(url_for('upload_file',
                                    filename=filename))

    return render_template('data.html',keys=request.args.get('filename'))#, l=secure_filename(file.filename))


app.secret_key = 'some_secret_key'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
# '192.168.1.233' port=8081
