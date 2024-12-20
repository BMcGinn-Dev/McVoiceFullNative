from flask import Flask, render_template, request, redirect, url_for
import os
import time

# Function to import functionalRun
def import_functionalRun():
    global functionalRun
    import functionalRun
    return functionalRun



# Create a new Flask application
app = Flask(__name__)

val_code = "000000"

# Define the path to save uploaded files
UPLOAD_FOLDER = 'UploadedPhoto'
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle the form submission and file upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        time.sleep(1)
        functionalRun = import_functionalRun()
        val_code = functionalRun.validation_code
        print(f"HERE IS THE FINAL CODE: {val_code}")
        return render_template('index.html', val_code=val_code)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
