import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import main

app = Flask(__name__)
UPLOAD_FOLDER = "data"
DOWNLOAD_FOLDER= "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

try:
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):  # Remove old files
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):  # Remove old files
        os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
except:
    pass

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    
    
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):  # Remove old files
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except:
        pass

    files = request.files.getlist('file')  # Get multiple files
    for file in files:
        if file.filename == '':
            return "No selected file"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    

    return "Files uploaded successfully!"


@app.route('/download',methods=['POST'])
def download_file():
    if request.method == 'POST':
        main.main()
        try:
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):  # Remove old files
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        except:
            pass
        

        return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'results.json',as_attachment=True)
    
    else: 
        return redirect(url_for('home'))
    
    
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.run(port=8000,debug=True)
