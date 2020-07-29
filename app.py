import csv
import os
# from collections import OrderedDict
# from csv import DictReader
# from typing import Dict, Union
from urllib.request import urlretrieve as retrieve
from werkzeug.utils import secure_filename
# from _collections import defaultdict

from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to connect our HTML file
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aboutus')
def about_us():
    return render_template('About.html')


@app.route('/bar')
def bar_page():
    return render_template('bartool.html')


@app.route('/horizontal')
def horizontal_page():
    return render_template('horizontalbartool.html')


@app.route('/pie')
def pie_page():
    return render_template('pietool.html')


@app.route('/line')
def line_page():
    return render_template('linetool.html')


@app.route('/doughnut')
def doughnut_page():
    return render_template('doughnuttool.html')


@app.route('/radar')
def radar_page():
    return render_template('radartool.html')


@app.route('/polararea')
def polar_area_page():
    return render_template('polarareatool.html')


# Function to get a COVID-19 data file and display the contents of it
@app.route('/covid')
def import_covid_csv():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    retrieve(url, 'covid_file/us.csv')

    with open('covid_file/us.csv', 'r') as covidfile:
        csv_read = csv.DictReader(covidfile)
        # print(csv_read)
        covid_list = []

        # For loop to get the last 7 days of Covid Data
        for j in list(reversed(list(csv_read)))[0:7]:
            # print(j)
            date = j['date']
            cases = j['cases']
            deaths = j['deaths']
            covid_list.append({'date': date, 'cases': cases, 'deaths': deaths})

        # Function to compute and display the COVID-19 death rate
        def compute_csv():
            data = []
            with open('covid_file/us.csv', 'r') as covidfile:
                csv_read = csv.DictReader(covidfile)
                for i in list(reversed(list(csv_read))):
                    # print(i)
                    cases = i['cases']
                    deaths = i['deaths']
                    rate = int(deaths) / int(cases)
                    data.append({'cases': cases, 'deaths': deaths, 'rate': rate})
                    return data

        return render_template('covid.html', l=covid_list, k=compute_csv())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_file():
    return render_template('index.html')


# Function to get a data file and display the contents of it
@app.route('/graph', methods=['GET', 'POST'])
def get_second_csv():
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
    return render_template('mapping.html')  # l=secure_filename(file.filename))


# except Upload_Error:
#     raise Exception('Upload Error')


# def compute_second_csv():
#    csv_data = []
#     with open('uploads/', filename) as second_file:
#         for i in list(reversed(list(second_file))):
#             print(i)

# cases = i['cases']
# deaths = i['deaths']
# rate = int(deaths) / int(cases)
# csv_data.append({'cases': cases, 'deaths': deaths, 'rate': rate})
# print(csv_data)

# compute_second_csv()

#
# return render_template('data.html')


app.secret_key = 'some_secret_key'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
# '192.168.1.233' port=8081
