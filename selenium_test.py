""" from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your ChromeDriver executable
chrome_driver_path = r'C:/Users/alere\Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Chrome options for more stable execution
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")  # This can be used instead of driver.maximize_window()

# Set up service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with options
driver = webdriver.Chrome(service=service, options=options)

try:    
    # URL to visit
    url = "https://chatgpt.com/auth/login?next=/g/g-2DQzU5UZl-code-copilot"
        
    # Navigate to the URL
    driver.get(url)


    # Optional: wait for a few seconds to view the page
    time.sleep(5)  # Adjust time as needed

finally:
    # Close the browser window
    driver.quit()

 """


for i in range(30):
    print(i)