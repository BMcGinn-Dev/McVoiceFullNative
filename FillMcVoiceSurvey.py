import time
import re
import os
from icecream import ic  # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from webdriver_manager.firefox import GeckoDriverManager  # type: ignore

full_val_code = ""


# Specify the folder and file name
folder_path = "SurveyCode"
file_name = os.listdir(folder_path)[0]  # Assumes only one file in the folder

# Construct the full file path
text_file = os.path.join(folder_path, file_name)


def openChromeBrowser():
    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument(
        "--window-size=1920,1080"
    )  # Set window size for headless mode
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Recommended for headless mode on Linux
    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )  # Avoid issues with shared memory

    # Setup Chrome WebDriver with options
    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # Open McDVoice website in Chrome
    chrome_driver.get("https://www.mcdvoice.com")

    return chrome_driver


def closeChromeBrowser(chrome_driver):
    # Close Chrome browser
    chrome_driver.quit()


def split_surv_code(text_file):
    """
    Opens a text file containing a survey code, reads the content, and splits the code into six parts
    based on the hyphen delimiter. Each part is returned as a separate variable.

    Args:
        text_file (str): The path to the text file containing the survey code.

    Returns:
        tuple: A tuple containing six elements, each representing a part of the survey code.
    """
    # Open the specified text file in read mode
    with open(text_file, "r") as file:
        # Read the entire content of the file into a string
        survey_code = file.read()

    # Split the survey code string into six parts using the hyphen as a delimiter
    # Each part is assigned to a separate variable (p1, p2, p3, p4, p5, p6)
    p1, p2, p3, p4, p5, p6 = survey_code.split("-")

    # IceCream Validation Check (commented out)
    # This line is used for debugging purposes to print the split parts
    # ic(p1, p2, p3, p4, p5, p6)

    # Return the six parts as a tuple
    return p1, p2, p3, p4, p5, p6


def extract_and_save_numbers(input_string):
    """
    Extract numbers from a formatted string and save them to a file named 'ValidationCode_#######.txt'.

    Args:
        input_string (str): The string containing the validation code.
    """
    # Use regex to find the numbers in the string
    match = re.search(r"\d+", input_string)

    if match:
        numbers = match.group()  # Extract the matched numbers
        print(f"Extracted numbers: {numbers}")

        # Dynamically name the file based on the extracted numbers
        file_name = f"ValidationCode/validation_code.txt"

        # Write the numbers to the dynamically named file
        with open(file_name, "w") as file:
            file.write(numbers)

        print(f"Numbers saved to {file_name}")
    else:
        print("No numbers found in the input string.")


# Empty for the moment
def fill_first_page(c_browser):

    c1, c2, c3, c4, c5, c6 = split_surv_code(text_file)
    # The survey code entry is 5 5-digit codes & 1 1-digit code
    # Codes_list contains the 6 segements of codes from the survey code
    codes_5_list = [c1, c2, c3, c4, c5]

    # Find all input elements with the class "coupon-length-5"
    input_elements = c_browser.find_elements(By.CLASS_NAME, "coupon-length-5")

    # Loop through each input element FOR THE 5 DIGIT LENGHTS
    for index, input_element in enumerate(input_elements):
        # Clear any existing text
        input_element.clear()

        # Enter the value based on index (e.g., #0, #1, etc.)
        input_element.send_keys(str(codes_5_list[index]))
        time.sleep(1)

    ic("5 Elements done.")

    # Find all input elements with the class "coupon-length-5"
    input_elements = c_browser.find_elements(By.CLASS_NAME, "coupon-length-1")

    # Loop through each input element FOR THE 1 DIGIT LENGHTS
    for index, input_element in enumerate(input_elements):
        # Clear any existing text
        input_element.clear()

        # Enter the value based on index (e.g., #0, #1, etc.)
        input_element.send_keys(str(c6))
        time.sleep(1)

    ic("1 Elements done.")

    # Find the "Start" button

    # Find all input elements with the class "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_second_page(c_browser):

    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000455.1"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_third_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R004000.2"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_fourth_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R001000.5"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_fifth_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000444.1"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


# Employee ask for mobile app + Greet by name
def fill_sixth_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Employee ask if using mobile app --> YES
    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000473.1"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Employee greet you by name --> NO
    # Ensure a specific element on the second page is present before proceeding
    radio_button = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000474.2"))
    )

    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_seventh_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # So here is where the survey can give you different questions. We need to try-except all the possible
    # questions they may have. We are going to get the whole page html and store it in an html file
    """
    try:
        # Scrape the entire HTML
        page_html = c_browser.page_source
        ic("HTML of the seventh page successfully scraped.")
        
        # Optionally save or process the HTML
        with open("seventh_page.html", "w", encoding="utf-8") as file:
            file.write(page_html)
        ic("HTML saved to 'seventh_page.html' for debugging.")
    except:
        ic("Couldnt save page for some reason...")
    """

    # Temperature of your food --> HS
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R006000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Temperature of your food Done.")
    except:
        pass

    # Freindliness of Employees --> HS
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R009000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Friendliness of Employees Done.")
    except:
        pass

    # Cleanliness of restaurant --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R000351.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Cleanliness of Restaurant Done.")
    except:
        pass

    # Ease of placing order --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R011000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Ease of placing order Done.")
    except:
        pass

    # Speed of Service --> Satisfied
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R008000.4"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Speed of Service Done.")
    except:
        pass

    # Quality of Food --> Satisfied
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R028000.4"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Quality of Food Done.")
    except:
        pass

    # Accuracy of order --> HighlySatisfied
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R007000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Accuracy of Order Done.")
    except:
        pass

    # Taste of Food --> HighlySatisfied
    try:

        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R005000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Taste of Food Done.")
    except:
        pass

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_eigth_page(c_browser):
    # Wait for the new page to fully load
    WebDriverWait(c_browser, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Temperature of your food --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R006000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Temperature of your food Done.")
    except:
        pass

    # Freindliness of Employees --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R009000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Friendliness of Employees Done.")
    except:
        pass

    # Cleanliness of restaurant --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R000351.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Cleanliness of Restaurant Done.")
    except:
        pass

    # Ease of placing order --> HS
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R011000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Ease of placing order Done.")
    except:
        pass

    # Speed of Service --> Satisfied
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R008000.4"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Speed of Service Done.")
    except:
        pass

    # Quality of Food --> Satisfied
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R028000.4"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Quality of Food Done.")
    except:
        pass

    # Accuracy of order --> HighlySatisfied
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R007000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Accuracy of Order Done.")
    except:
        pass

    # Taste of Food --> HighlySatisfied
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R005000.5"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Taste of Food Done.")
    except:
        pass

    # Overall value for price you paid --> HighlySatisfied
    try:
        radio_button = WebDriverWait(c_browser, 10).until(
            EC.presence_of_element_located((By.ID, "R015000.3"))
        )
        # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
        c_browser.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)
        ic("Overall value of food Done")
    except:
        pass

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_ninth_page(c_browser):
    # Which of the following did you order (checkboxes) --> Burgers, Chicken, Fish

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000505"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Burgers, Chicken, Fish Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_tenth_page(c_browser):
    # Which of the following did you order (checkboxes) --> Big Mac

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000518"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Big Mac Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_eleventh_page(c_browser):
    # The quality of your Big Mac --> HS

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000425.5"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Big Mac Quality Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_twelfth_page(c_browser):
    # Did you experience a problem during your visit? --> No

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R016000.2"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Problem? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_thirteenth_page(c_browser):
    # Recommend this McDonalds in 30 days? --> Likely

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R018000.4"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Recommend McDonalds? Done.")

    # Return to this McDonalds in 30 days? --> Likely

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R019000.4"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Return to McDonalds? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_fourteenth_page(c_browser):
    # Write a review --> Just click the next button, we will just wait for 5 seconds
    time.sleep(5)

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_fifthteenth_page(c_browser):
    # Did you have to pull ahead at the drive thru? --> No

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000026.2"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Pull Ahead at drive thru? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_sixteenth_page(c_browser):
    # How many times have you visted McDonalds in the last 30 Days? --> 2

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R020000.2"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Pull Ahead at drive thru? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_seventeenth_page(c_browser):
    # Which of the following restaurant is your favorite --> McDonalds

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000387.4"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Favorite Restaurant? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_eighteenth_page(c_browser):
    # McDonalds is a brand I trust --> Strongly agree

    check_box = WebDriverWait(c_browser, 10).until(
        EC.presence_of_element_located((By.ID, "R000482.5"))
    )
    # Click the radio button --> Apparently the site is JavaScript-Controlled & this is you trigger a click in Javascript
    c_browser.execute_script("arguments[0].click();", check_box)
    time.sleep(1.5)
    ic("Favorite Restaurant? Done.")

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_nineteenth_page(c_browser):
    # Annual household income --> 100k+
    # Also totally optional, can just skip
    time.sleep(2)

    """
    # Locate the dropdown element by its ID
    dropdown = c_browser.find_element("id", "R024000")

    # Create a Select object
    select = Select(dropdown)

    # Select the option with value '6' (100,000 or more)
    select.select_by_value("6")
    
    time.sleep(.3)
    """

    # Find the input "NextButton"
    next_button = c_browser.find_element(By.CLASS_NAME, "NextButton")
    # Simulate hitting "Enter" on the button
    next_button.send_keys(Keys.ENTER)


def fill_final_page(c_browser):
    # Displays validation code --> class name = "ValCode"
    time.sleep(1)

    # Find the element by class name
    valcode_element = c_browser.find_element(By.CLASS_NAME, "ValCode")
    ic("We have the validation code!!")
    ic(valcode_element.text)

    time.sleep(2)
    # print(valcode_element.text)
    # print(valcode_element.get_attribute("innerHTML"))
    return valcode_element.text


# ______________ ACTION TIME ___________________________


# ic(c1, c2, c3, c4, c5, c6)

# Begin Try-Excepts for each of the survey pages

try:
    c_browser = openChromeBrowser()
except:
    ic("Failed to initialize Chrome Browser with Selenium.")

time.sleep(1)

print(("-" * 50) + "Browser initiated")

# Try first page
print(("-" * 50) + "1st Page")
try:
    fill_first_page(c_browser)
    ic("Successful completion of 1st Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 1st page.")

# Try second page
print(("-" * 50) + "2nd Page")
try:
    fill_second_page(c_browser)
    ic("Successful completion of 2nd Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 2nd page.")

# Try third page
print(("-" * 50) + "3rd Page")
try:
    fill_third_page(c_browser)
    ic("Successful completion of 3rd Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 3rd page.")

# Try fourth page
print(("-" * 50) + "4th Page")
try:
    fill_fourth_page(c_browser)
    ic("Successful completion of 4th Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 4th page.")

# Try fifth page
print(("-" * 50) + "5th Page")
try:
    fill_fifth_page(c_browser)
    ic("Successful completion of 5th Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 5th page.")

# Try sixth page
print(("-" * 50) + "6th Page")
try:
    fill_sixth_page(c_browser)
    ic("Successful completion of 6th Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 6th page.")

# Try seventh page
print(("-" * 50) + "7th  Page")
try:
    fill_seventh_page(c_browser)
    ic("Successful completion of 7th Page")
except Exception as e:
    ic("Failed to fill seventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 7th page.")
time.sleep(1.5)

# Try eight page --> The 8th page is just an extension of the seventh page, questions not asked on 7 are asked on 8 (except for overall value)
# Takes a bit long because it rechecks them all but we are totally good
print(("-" * 50) + "8th  Page")
try:
    fill_eigth_page(c_browser)
    ic("Successful completion of 8th Page")
except Exception as e:
    ic("Failed to fill eight survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 8th page.")
time.sleep(1.5)

# Try ninth page
print(("-" * 50) + "9th  Page")
try:
    fill_ninth_page(c_browser)
    ic("Successful completion of 9th Page")
except Exception as e:
    ic("Failed to fill ninth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 9th page.")
time.sleep(1.5)

# Try tenth page
print(("-" * 50) + "10th  Page")
try:
    fill_tenth_page(c_browser)
    ic("Successful completion of 10th Page")
except Exception as e:
    ic("Failed to fill tenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 10th page.")
time.sleep(1.5)

# Try eleventh page
print(("-" * 50) + "11th  Page")
try:
    fill_eleventh_page(c_browser)
    ic("Successful completion of 11th Page")
except Exception as e:
    ic("Failed to fill eleventh survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 11th page.")
time.sleep(1.5)

# Try twelfth page
print(("-" * 50) + "12th  Page")
try:
    fill_twelfth_page(c_browser)
    ic("Successful completion of 11th Page")
except Exception as e:
    ic("Failed to fill twelfth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 12th page.")
time.sleep(1.5)

# Try 13th page
print(("-" * 50) + "13th  Page")
try:
    fill_thirteenth_page(c_browser)
    ic("Successful completion of 11th Page")
except Exception as e:
    ic("Failed to fill thirteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 13th page.")
time.sleep(1.5)

# Try 14th page
print(("-" * 50) + "14th  Page")
try:
    fill_fourteenth_page(c_browser)
    ic("Successful completion of 11th Page")
except Exception as e:
    ic("Failed to fill fourteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 14th page.")
time.sleep(1.5)

# Try 15th page
print(("-" * 50) + "15th  Page")
try:
    fill_fifthteenth_page(c_browser)
    ic("Successful completion of 15th Page")
except Exception as e:
    ic("Failed to fill fifthteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 15th page.")
time.sleep(1.5)

# Try 16th page
print(("-" * 50) + "16th  Page")
try:
    fill_sixteenth_page(c_browser)
    ic("Successful completion of 16th Page")
except Exception as e:
    ic("Failed to fill sixteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 16th page.")
time.sleep(1.5)

# Try 17th page
print(("-" * 50) + "17th  Page")
try:
    fill_seventeenth_page(c_browser)
    ic("Successful completion of 17th Page")
except Exception as e:
    ic("Failed to fill seventeenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 17th page.")
time.sleep(1.5)

# Try 18th page
print(("-" * 50) + "18th  Page")
try:
    fill_eighteenth_page(c_browser)
    ic("Successful completion of 18th Page")
except Exception as e:
    ic("Failed to fill eighteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 18th page.")
time.sleep(1.5)

# Try 19th page
print(("-" * 50) + "19th  Page")
try:
    fill_nineteenth_page(c_browser)
    ic("Successful completion of 19th Page")
except Exception as e:
    ic("Failed to fill nineteenth survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish 19th page.")
time.sleep(1.5)

# Try final page
print(("-" * 50) + "Final  Page")
try:
    validation_code = fill_final_page(c_browser)
    ic("Successful completion of Finals Page")
except Exception as e:
    ic("Failed to fill Final survey page. Run in vacuum.")
    ic(f"Here is the exception: \n {e}")
finally:
    ic("Completed attempt to finish Final page.")
time.sleep(1.5)

# Validation code text is returend as: "Validation Code: #######"
# Extract the numbers and create a .txt containing only the code
print(("-" * 50) + "Outputting to .txt")
try:
    extract_and_save_numbers(validation_code)
    full_val_code = validation_code
    ic("Successfully outputted Validation Code to text file")
except:
    ic("Failed to output Validation Code to text")


ic(full_val_code)
print("Closing program...")
time.sleep(1)
closeChromeBrowser(c_browser)
