import os
from urllib.request import urlretrieve as retrieve
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to display our home page
@app.route('/')
def index():
    return render_template('index.html')


# Function to display our about us page
@app.route('/aboutus')
def about_us():
    return render_template('About.html')


# Function to only allow CSV file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to redirect filename
@app.route('/upload')
def upload_file():
    return redirect(url_for('get_csv', filename=upload_file))


# Function to get/upload a user data file in the /uploads directory to then analyze in Jupyter Notebooks
# This function also gets a sample COVID-19 data file from The NY Times Github repo
@app.route('/uploader', methods=['GET', 'POST'])
def get_csv():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    retrieve(url, 'covid_file/us.csv')

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

    return render_template('data.html', keys=request.args.get('filename'))


app.secret_key = 'some_secret_key'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
# '192.168.1.233' port=8081
