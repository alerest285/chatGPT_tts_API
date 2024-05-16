import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Sets up the Chrome driver with specific options."""
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    print("Configuring Chrome driver with debugger address...")
    return webdriver.Chrome(options=options)

def navigate_to_page(driver, url):
    """Navigates to a given URL using the specified driver."""
    print(f"Navigating to {url}...")
    driver.get(url)

def wait_for_element_stability(driver, xpath, max_retries=5, delay=2):
    """Attempt to find the element multiple times until it is stable or retries are exhausted."""
    print(f"Attempting to stabilize element at {xpath}...")
    for attempt in range(max_retries):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"Element found, checking for stability (Attempt {attempt+1})...")
            time.sleep(delay)  # Wait to see if the element remains stable
            current_text = element.text
            if current_text and current_text.strip():  # Check if text is non-empty and seems stable
                print("Element is stable.")
                return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to find or stabilize element (Attempt {attempt+1}): {e}")
            time.sleep(delay)  # Wait before retrying
    print("Element did not stabilize after multiple attempts.")
    return None

def send_prompt_to_chatbot(driver, prompt, n):
    """Sends a prompt to the chatbot and retrieves the response."""
    print(f"Sending prompt '{prompt}'...")
    xpath_textarea = '//*[@id="prompt-textarea"]'
    xpath_inputbutton = '//*[@id="__next"]/div[1]/div/main/div[1]/div[2]/div[2]/div/form/div/div[2]/div/div/button'
    try:
        textarea = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_textarea))
        )
        textarea.click()  # Ensure the textarea is focused before sending keys
        textarea.clear()  # Clear any existing text
        textarea.send_keys(prompt + Keys.TAB + Keys.ENTER)
        """ inputbutton = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_inputbutton))
        )
        inputbutton.click() """
        print("Prompt sent successfully.")
    except TimeoutException:
        print("Failed to find the textarea within the given timeout.")
        return None

    # Construct the XPath for the response based on the incrementing 'n' value
    xpath_response = f'//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/div[{n}]/div/div/div[2]/div/div[1]/div/div/div/p'
    response_element = wait_for_element_stability(driver, xpath_response)
    if response_element:
        response_text = response_element.text
        print(f"Received response: {response_text}")
        return response_text
    else:
        print("No stable response received.")
        return None

def main():
    driver = setup_driver()
    try:
        navigate_to_page(driver, "https://chatgpt.com/g/g-prR5hdsQU-french-teacher")
        responses = [
            ("init", 3),
            ("bonjour, je voudrais parler", 5),
            ("sur la vie", 7),
            ("comme tu trouves la vie", 9),
            ("bonne nuit, je sors maintenant", 11)
        ]
        for prompt, n in responses:
            response_text = send_prompt_to_chatbot(driver, prompt, n)
            if response_text:
                print(response_text)
            else:
                print("Skipping due to no response or stabilization issue.")
    finally:
        print("Closing driver.")
        driver.quit()

if __name__ == "__main__":
    main()

