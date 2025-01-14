import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set your Google API key for generative AI
genai.configure(api_key="AIzaSyA8f29-IrMjt3oYwr_Z81D3ciDhJtOuvr0")  

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate model name

# Global flag to stop speech
stop_speech = False

# Function to listen for a command
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return ""

# Function to speak out text and stop if necessary
def speak(text):
    global stop_speech
    stop_speech = False  # Reset the stop flag each time a new message is spoken

    # Stop any ongoing speech before speaking new text
    if engine.isBusy():
        engine.stop()

    # Start speaking the new text
    engine.say(text)
    engine.runAndWait()

# Function to stop the speech
def stop_speaking():
    global stop_speech
    stop_speech = True
    engine.stop()  # Stop current speaking immediately

# Function to get a response from Google’s Generative AI (Gemini)
def get_ai_response(query):
    try:
        response = model.generate_content(query)
        ai_response = response.text.strip()
        print(f"AI response: {ai_response}")  # Debug: print AI response
        return ai_response
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Sorry, I couldn't process that request."

# Main program
def main():
    while True:
        command = listen_for_command()

        if "open chat mode" in command:
            speak("Chat mode activated. Ask me anything!")
            print("Chat mode activated.")  # Debug
            while True:
                question = listen_for_command()
                if "exit chat mode" in question:
                    speak("Exiting chat mode.")
                    break
                if "stop" in question:  # If "stop" command is given, stop the current speech
                    stop_speaking()
                    speak("Speech stopped.")
                    continue
                if question:
                    print(f"Question received: {question}")  # Debug
                    response = get_ai_response(question)
                    speak(response)
                else:
                    print("No question detected.")  # Debug
        elif "exit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
