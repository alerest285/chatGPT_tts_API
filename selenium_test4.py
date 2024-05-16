from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

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

def wait_for_prompt_stability(driver, xpath, timeout=30):
    """Wait until the text at the given xpath is stable for a certain period."""
    old_text = None
    stable_time_required = 3  # seconds the text must remain stable
    last_change_time = time.time()
    print(f"Checking for stability of element at {xpath}...")

    while time.time() - last_change_time == last_change_time < timeout:
        try:
            current_text = driver.find_element(By.XPATH, xpath).text
            if current_text == old_text:
                if time.time() - last_change_time >= stable_time_required:
                    print("Element is stable.")
                    return True
            else:
                last_change_time = time.time()
            old_text = current_text
            time.sleep(0.5)
        except Exception as e:
            print(f"Error during stability check: {e}")
            break
    print("Element did not stabilize in time.")
    return False

def send_prompt_to_chatbot(driver, prompt, n):
    """Sends a prompt to the chatbot and retrieves the response after ensuring the prompt is stable."""
    print(f"Sending prompt '{prompt}'...")
    if prompt != "init":
        xpath_responsearea = f'//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/div[{n}]/div/div/div[2]/div/div[1]/div/div/div/p'
        if not wait_for_prompt_stability(driver, xpath_responsearea):
            print("Prompt did not stabilize in time.")
            return None
    
    xpath_textarea = '//*[@id="prompt-textarea"]'
    try:
        textarea = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_textarea))
        )
        textarea.click()  # Focus the textarea
        textarea.send_keys(prompt + Keys.ENTER)

        xpath_response = f'//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/div[{n}]/div/div/div[2]/div/div[1]/div/div/div/p'
        response = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_response))
        )
        response_text = " ".join(element.text for element in driver.find_elements(By.XPATH, xpath_response))
        print(f"Received response: {response_text}")
        return response_text
    except TimeoutException:
        print("Failed to send prompt or receive response within timeout.")
    except NoSuchElementException:
        print("Required element not found on the page.")

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
            if response_text is not None:
                print(response_text)
            else:
                print("No response received, skipping...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
