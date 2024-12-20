# So one of the 'issues' I am facing is that when I import easyOCRExtract & FillMcVoiceSurvey
#  it runs them immediately before any of the values get called in the function, I'd prefer they do not
#  run until they get actually called, will have to look into that


import os
from shutil import move
from flask import Flask, request, render_template, jsonify
from icecream import ic  # type: ignore

# Delayed import of easyOCRExtract and FillMcVoiceSurvey
easyOCRExtract = None
FillMcVoiceSurvey = None


# Function to import easyOCRExtract
def import_easyOCRExtract():
    global easyOCRExtract
    if easyOCRExtract is None:
        import easyOCRExtract
    return easyOCRExtract


# Function to import FillMcVoiceSurvey
def import_FillMcVoiceSurvey():
    global FillMcVoiceSurvey
    if FillMcVoiceSurvey is None:
        import FillMcVoiceSurvey
    return FillMcVoiceSurvey


# ________________________________________________________________________________________________________________________


# Run the OCR script to get the initial survey code: final_survey_code
# This outputs a .txt file to SurveyCode/
ic("Beginning the survey code extraction...")
easyOCRExtract = import_easyOCRExtract()
initial_survey_code = easyOCRExtract.serv_code
ic("Finished Survey Code generation.")
ic(initial_survey_code)


# Now we use that survey code to run the headless, survey completion script
# This may take awhile...
ic("Beginning the validation code extraction...")
FillMcVoiceSurvey = import_FillMcVoiceSurvey()
validation_code = FillMcVoiceSurvey.full_val_code
ic("Finished Validation Code extraction.")
validation_code = "".join(filter(str.isdigit, validation_code))
ic(validation_code)
print(f"Here is your final discount code: {validation_code}")


ic("The survey is now complete.")
