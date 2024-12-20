from flask import Flask, render_template, request, redirect, url_for
import os
import time


# Function to import functionalRun
def import_functionalRun():
    global functionalRun
    import functionalRun

    return functionalRun


def clear_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Create a new Flask application
app = Flask(__name__)

val_code = "000000"

# Define the path to save uploaded files
UPLOADED_PHOTO_FOLDER = "UploadedPhoto"
VALIDATION_CODE_FOLDER = "ValidationCode"
SURVEY_CODE_FOLDER = "SurveyCode"
# Ensure the upload folder exists
if not os.path.exists(UPLOADED_PHOTO_FOLDER):
    os.makedirs(UPLOADED_PHOTO_FOLDER)

# Configure the upload folder
app.config["UPLOADED_PHOTO_FOLDER"] = UPLOADED_PHOTO_FOLDER


# Define a route for the root URL
@app.route("/")
def index():
    return render_template("index.html")


# Define a route to handle the form submission and file upload
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        # Save the file to the upload folder
        file_path = os.path.join(app.config["UPLOADED_PHOTO_FOLDER"], file.filename)
        file.save(file_path)
        time.sleep(1)
        try:
            functionalRun = import_functionalRun()
            val_code = functionalRun.validation_code
        except:
            print('some error occured in functionalRun.py')
            clear_folder(UPLOADED_PHOTO_FOLDER)
            clear_folder(VALIDATION_CODE_FOLDER)
            clear_folder(SURVEY_CODE_FOLDER)
            val_code = "ERROR, clearing uploads"
        print(f"HERE IS THE FINAL CODE: {val_code}")
        return render_template("index.html", val_code=val_code)


@app.route("/clear", methods=["POST"])
def clear_files():
    clear_folder(UPLOADED_PHOTO_FOLDER)
    clear_folder(VALIDATION_CODE_FOLDER)
    clear_folder(SURVEY_CODE_FOLDER)
    return redirect(url_for("index"))


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
