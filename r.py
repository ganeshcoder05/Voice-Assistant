import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time

# --- Configuration ---
ASSISTANT_NAME = " Kirava"

# --- Initialization ---
# Initialize the Text-to-Speech engine
engine = pyttsx3.init() # 'sapi5' is the Microsoft Speech API. On Linux/Mac, this might vary.
voices = engine.getProperty('voices')

# Set voice (0 is usually male, 1 is usually female on Windows)
engine.setProperty('voice', voices[0].id) 
# You can adjust the rate (speed) of speech
engine.setProperty('rate', 190)

def speak(text):
    """Converts text to speech"""
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Greets the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak(f"I am {ASSISTANT_NAME}. How may I help you?")

def take_command():
    """
    Listens to microphone input and returns it as string.
    Returns 'None' if audio is unintelligible.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # Seconds of non-speaking audio before a phrase is considered complete
        r.energy_threshold = 300 # Minimum audio energy to consider for recording
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e) # Uncomment to see specific error
        print("Say that again please...")
        return "None"
    
    return query.lower()

def main():
    """Main execution loop"""
    wish_me()
    
    while True:
        query = take_command()

        # Logic for executing tasks based on query
        if query == "none":
            continue

        # 1. Wikipedia Search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("I couldn't find a page for that topic.")
            except wikipedia.exceptions.DisambiguationError:
                speak("There were too many results, please be more specific.")

        # 2. Open Websites
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")
            
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        # 3. Tell Time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        # 4. Open Application (Example: Notepad)
        # Note: You need to fix the path to match your specific system
        elif 'open notepad' in query:
            speak("Opening Notepad")
            # Example path for Windows
            os.startfile("C:\\Windows\\system32\\notepad.exe") 

        # 5. Exit the program
        elif 'quit' in query or 'exit' in query or 'stop' in query:
            speak("Goodbye, have a nice day!")
            break

if __name__ == "__main__":
    main()