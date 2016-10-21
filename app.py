import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from evaluatework import evaluateWork
import _thread
import time


UPLOAD_FOLDER = 'submits'
ALLOWED_EXTENSIONS = set(['java'])
INSTRUCTOR_PASSWORD = 'twiddlesticks'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['INSTRUCTOR_PASSWORD'] = INSTRUCTOR_PASSWORD

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            _thread.start_new_thread(evaluateWork,(filename,request.form['name']))
            return "Thanks bro"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
        <input name=name>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/results.dat')
def getResults():
    _thread.start_new_thread(deleteFileAfterDelay,("results.dat",2))
    return send_file("results.dat")

def deleteFileAfterDelay(file,delay):
    time.sleep(delay)
    os.remove(file)

@app.route('/tests.dat')
def getTests():
    return send_file("tests.dat")

@app.route('/sendTests', methods=['GET', 'POST'])
def sendTests():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save("tests.dat")
            return "Thanks bro"
    return '''
    <!doctype html>
    <title>Upload new Test</title>
    <h1>Upload new Test</h1>
    <form action="sendTests" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)