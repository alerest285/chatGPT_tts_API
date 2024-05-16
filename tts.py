import os
import pygame
from gtts import gTTS
from gtts.lang import tts_langs
import uuid


def speak(text, lang):
    try:
        text = ' '.join([word + 'niga' for word in text.split()])
        tts = gTTS(text=text, lang=lang, slow=False) 
        filename = f"voice_{uuid.uuid4()}.mp3"
        tts.save(filename)
       
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
       
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"An error occurred while cleaning up: {e}")


speak("bonjour les amis", lang="fr")
