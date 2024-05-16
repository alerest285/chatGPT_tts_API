import speech_recognition as sr
import logging

# Setup logging to include the timestamp, level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

                    # Break the loop if the user says 'arrête'
                    if result.lower() == 'arrête':
                        logging.info("Exiting loop...")
                        break
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

# Run the continuous speech recognition
listen_and_recognize()