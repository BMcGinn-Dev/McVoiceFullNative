import os
import easyocr  # type: ignore
import cv2  # type: ignore
from icecream import ic # type: ignore

# Specify the folder and file name
folder_path = "UploadedPhoto"
file_name = os.listdir(folder_path)[0]  # Assumes only one file in the folder

# Construct the full file path
image_path = os.path.join(folder_path, file_name)

ic(image_path)

def check_image_health(image_path):

    # Check if file exists
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
    except FileNotFoundError as e:
        print(e)
        exit("System exiting...")

    # Check if the image loads with OpenCV
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image failed to load. Check the file path or format.")
    except ValueError as e:
        print(e)
        exit("System exiting...")
    else:
        print("~ Image loaded successfully by OpenCV.")
        # print(f"Image dimensions: {img.shape}")


def perform_OCR(image_path):
    # Convert image path (string val) to an img (image object)
    img = cv2.imread(image_path)

    # Convert the image to grayscale as required by EasyOCR
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize the EasyOCR reader
    try:
        reader = easyocr.Reader(["en"])
    except:
        print("Some issue reading the imager in EasyOCR\n")
        exit("System exiting...")

    # Perform OCR
    results = reader.readtext(img_gray)
    print(f"~ OCR Successful.")
    return results


def output_OCR_results(results):
    # Output the results
    for idx, (bbox, text, confidence) in enumerate(results):
        # print(f"{idx}: Detected text: {text} (Confidence: {confidence})")
        if "Survey" in text:
            # print(idx, text)

            survey_code_txt = results[idx + 1][1]  # Get the text of the next index
            # print(f"{idx + 1}: {survey_code_txt}")

            print("~ Survey Code Stored.")
    return survey_code_txt


def write_servCode_to_txt(serv_code):
    # Write the survey code to a text file
    file_name = "SurveyCode/survey_code_" + serv_code + ".txt"

    with open(file_name, "w") as file:
        file.write(serv_code)

    print(f"~ Survey code: {serv_code} has been written to {file_name}")



# Check Image Health --> Perform OCR --> Get survey code text --> Store as unique .txt file
print("-" * 35)
check_image_health(image_path)
OCR_result = perform_OCR(image_path)
serv_code = output_OCR_results(OCR_result)
write_servCode_to_txt(serv_code)
print("Survey Code Extraction Complete.")
print("-" * 35)
