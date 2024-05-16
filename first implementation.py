from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import speech_recognition as sr
import logging
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def listen_and_recognize(timeout=15, language='fr-FR', pause_threshold=2):
    # Initialize the recognizer
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            while True:
                logging.info("Listening for speech in French... (say 'arrête' to stop)")

                # Adjust for ambient noise and set the pause threshold
                r.adjust_for_ambient_noise(source, duration=0.2)
                r.pause_threshold = pause_threshold

                try:
                    audio = r.listen(source, timeout=timeout)
                    result = r.recognize_google(audio, language=language)
                    logging.info(f"Google Speech Recognition thinks you said: {result}")
                    return(result)

                except sr.WaitTimeoutError:
                    logging.info(f"No speech was detected within {timeout} seconds.")
                except sr.UnknownValueError:
                    logging.info("Google Speech Recognition could not understand the audio.")
                except sr.RequestError as e:
                    logging.error(f"Could not request results from Google Speech Recognition service; {e}")
                    
    except KeyboardInterrupt:
        logging.info("Loop has been stopped by a user.")
    except Exception as e:
        logging.exception("An unexpected error occurred:")
    finally:
        logging.info("Cleanup can be done here.")

def main():

    os.popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\localhost"')

    driver = setup_driver()
    i = 0

    try:
        navigate_to_page(driver, "https://chatgpt.com/?model=text-davinci-002-render-sha")
        while True:
            prompt = listen_and_recognize()
            # Break the loop if the user says 'arrête'
            if prompt.lower() == 'arrête':
                logging.info("Exiting loop...")
                break
            response_text = send_prompt_to_chatbot(driver, prompt, 3 + (i*2))
            if response_text:
                print(response_text)
                i += 1
            else:
                print("Skipping due to no response or stabilization issue.")
    finally:
        print("Closing driver.")
        driver.quit()

if __name__ == "__main__":
    main()











