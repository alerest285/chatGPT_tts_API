from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException  # Importing the exception

def setup_driver():
    """Sets up the Chrome driver with specific options."""
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    return webdriver.Chrome(options=options)

def navigate_to_page(driver, url):
    """Navigates to a given URL using the specified driver."""
    driver.get(url)
    

def send_prompt_to_chatbot(driver, prompt, n):
    """Sends a prompt to the chatbot and returns the bot's response, with improved error handling."""
    xpath_textarea = '//*[@id="prompt-textarea"]'
    try:
        textarea = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_textarea))
        )
        textarea.click()  # Focus the textarea
        textarea.send_keys(prompt)
        driver.implicitly_wait(1)
        textarea.send_keys(Keys.CONTROL+Keys.ENTER)

        xpath_response = '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/div['+str(n)+']/div/div/div[2]/div/div[1]/div/div/div/p'
        response = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_response))
            
        )
        # Retrieve the full text from the response, handling cases where text might be split into multiple elements
        driver.implicitly_wait(5)
        if prompt != "init":
             return " ".join(response.text for response in driver.find_elements(By.XPATH, xpath_response))
        else:
            return None
    except TimeoutException:
        print("Failed to locate an element within the provided time.")
        return None

def main():
    driver = setup_driver()
    navigate_to_page(driver, "https://chatgpt.com/g/g-prR5hdsQU-french-teacher")
    response_text = send_prompt_to_chatbot(driver, "bonjour", 3) #initializing first response
    print(response_text)
    for i in range(1, 4):
        response_text = send_prompt_to_chatbot(driver, "dit mois une phrase commun", 3+(i*2))
        print(response_text)


    print(response_text)
    driver.quit()

if __name__ == "__main__":
    main()
