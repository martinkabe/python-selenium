import platform
from flask import Flask, send_file, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # This adds chromedriver binary to path automatically
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

## selenium version 4.25.0

app = Flask(__name__)


@app.route("/post_json", methods=['POST'])
def process_json():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
    else:
        return 'Content-Type not supported!'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cloud-policy")  # Disables cloud policy
    options.add_argument("--disable-features=CloudPolicy")  # Disables cloud management features
    options.add_argument('--ignore-certificate-errors')
    
    # Check the OS and set the appropriate ChromeDriver path
    if platform.system() == "Windows":
        service = Service(executable_path=r'selenium/chromedriver.exe')
    elif platform.system() == "Linux":
        service = Service(executable_path=r'/usr/bin/chromedriver')
    else:
        raise OSError("Unsupported operating system")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com/")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'L2AGLb')))
        approve_element = driver.find_element(By.ID, 'L2AGLb')
        approve_element.click()

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf')))
        input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(json['arg_1'] + Keys.ENTER)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, json['arg_1'])))

        driver.save_screenshot("figures/snapshot.png")
        return send_file("figures/snapshot.png")
    finally:
        driver.quit()  # Ensure the driver quits after the request


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # hello_world()
