# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
import requests
import base64
import json
from io import BytesIO as _BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import os
  
# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploaded_images'
ALLOWED_EXTENSIONS = {'jpeg','jpg','png'}


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def is_server_working():
    return 'Server Works'

@app.route('/upload_image', methods=['POST'])
def upload_image():
   if request.method == 'POST':
       filename = request.json['filename']
       print("filename:"+filename)
       filedata_base64 = request.json['filedata']
       trimmed_data = filedata_base64.split(",")[1]
       trimmed_info = filedata_base64.split(",")[0]
       with open(f'{UPLOAD_FOLDER}/{filename}','wb') as f:
           # f.write(filedata_base64)
           f.write(base64.b64decode(trimmed_data))
       with open(f'{UPLOAD_FOLDER}/{filename}.base64','w') as f:
           # f.write(filedata_base64)
           f.write(trimmed_info)

   return filename

@app.route('/get_image',methods=['GET'])
def get_image():
    filedata=None
    if request.method == 'GET':
        filename = request.args['filename']
        if (filename=='Status: Not Uploaded' or filename=='{}'):
            return ''
        print(f'{UPLOAD_FOLDER}/{filename}')
        with open(f'{UPLOAD_FOLDER}/{filename}', 'rb') as f:
            # f.write(filedata_base64)
            raw_bytes_data = f.read()
            filedata = base64.b64encode(raw_bytes_data).decode('utf-8')
        with open(f'{UPLOAD_FOLDER}/{filename}.base64', 'r') as f:
            # f.write(filedata_base64)
            base64_hdr_info = f.read()
        filedata = base64_hdr_info + ',' + filedata
    return filedata

'''
1.Delete option
2.Number shift ho jaaye
3.Summary Statistics
4. 
''''#


# @app.route('/upload_file', methods=['POST'])
# def index():
#    if request.method == 'POST':
#        if 'file' not in request.files:
#            print('No file attached in request')
#            return {"success":0}
#        file = request.files['file']
#        if file.filename == '':
#            print('No file selected')
#            return redirect(request.url)
#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
#            return redirect(url_for('uploaded_file', filename=filename))
#    return render_template('index.html')

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(debug=True,host='0.0.0.0')