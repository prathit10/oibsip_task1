import speech_recognition as sr
from gtts import gTTS
import pygame
import datetime
import webbrowser
import os
import tempfile

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You :", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print("Assistant:", response_text)
    tts = gTTS(text=response_text, lang='en')

    # temporary directory to save the mp3 file
    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, "response.mp3")
        try:
            tts.save(save_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(save_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        #  to stop music and quit mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def main():
    while True:
        command = listen_for_command()

        if command is None:
            continue  # Skip processing if command is None
        
        if command == "hello there":
            respond("Hello friend! How can I assist you today?")
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            respond("The current time is " + current_time)
        elif "date" in command:
            current_date = datetime.date.today().strftime("%B %d, %Y")
            respond("Today's date is " + current_date)
        elif "search" in command:
            query = command.replace("search", "").strip()
            url = "https://www.google.com/search?q=" + query
            webbrowser.open(url)
            respond("Here are the search results for " + query)
        elif "exit" in command:
            respond("Goodbye!")
            break  # Exit the loop immediately after saying goodbye
        else:
            respond("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
