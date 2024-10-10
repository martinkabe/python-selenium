import platform
from flask import Flask, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # This adds chromedriver binary to path automatically
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

## selenium version 4.25.0

app = Flask(__name__)


@app.route("/")
def hello_world():
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
        driver.save_screenshot("figures/spooky.png")
        return send_file("figures/spooky.png")
    finally:
        driver.quit()  # Ensure the driver quits after the request


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # hello_world()
