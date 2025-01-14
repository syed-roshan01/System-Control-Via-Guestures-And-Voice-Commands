import os
import speech_recognition as sr
import pyttsx3

# Initialize the speech engine for voice output
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return None

# Main function to start the interaction
def select_option():
    speak("Please select an option. Option 1: Chatbot Mode. Option 2: Cursor control using Hand Gesture. Option 3: Cursor control using Eye Gesture. Option 4: Voice Access")
    print("Please select an option:")
    print("Option 1 - Chatbot Mode")
    print("Option 2 - Cursor Control using Hand Gesture")
    print("Option 3 - Cursor Control using Eye Gesture")
    print("Option 4 - Voice Access")

    choice = listen()

    if choice:
        if "option 1" in choice:
            speak("You chose Chatbot Mode.")
            os.system("python chatbot.py")
        elif "option 2" in choice:
            speak("You chose Cursor Control using Hand Gesture.")
            os.system("python test4.py")
        elif "option 3" in choice:
            speak("You chose Cursor Control using Eye Gesture.")
            os.system("python eye.py")
        elif "option 4" in choice:
            speak("You chose Voice Access")
            os.system(r'start "" "C:\Windows\System32\VoiceAccess.exe"')
        else:
            speak("Sorry, I didn't understand your choice. Please try again.")
            select_option()
    else:
        speak("Sorry, I couldn't hear your choice. Please try again.")
        #select_option()

# Function to wait for the "start" command
def wait_for_start():
    speak("Say 'start' to begin.")
    while True:
        command = listen()
        if command and "start" in command:
            speak("Starting the program.")
            select_option()
            break
        else:
            speak("I am waiting for you to say 'start.'")

if __name__ == "__main__":
    wait_for_start()
