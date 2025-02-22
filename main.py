import speech_recognition as sr
import os
import webbrowser
import requests
from config import apikey  # Assuming you store the Google Gemini API key here
import datetime
import random
import numpy as np
import pyttsx3
from datetime import date
import openai

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

chat_history = []

def chat(query):
    global chat_history
    print(chat_history)

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyC25BXJLMzuqx7XZQD0fGKaME93O669FwY",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raise an error for bad status codes
        response_json = response.json()
        
        if 'contents' in response_json and len(response_json['contents']) > 0:
            reply = response_json['contents'][0]['parts'][0]['text']
            say(reply)
            chat_history.append({"role": "user", "content": query})
            chat_history.append({"role": "assistant", "content": reply})
            return reply
        else:
            say("Sorry, I didn't get a valid response.")
            return "Sorry, I didn't get a valid response."
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        say("Sorry, I couldn't connect to the AI service.")
        return "Sorry, I couldn't connect to the AI service."
    except ValueError as e:
        print(f"JSON decode error: {e}")
        print("Response content:", response.text)
        say("Sorry, I received an invalid response from the AI service.")
        return "Sorry, I received an invalid response from the AI service."

def ai(prompt):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyC25BXJLMzuqx7XZQD0fGKaME93O669FwY",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raise an error for bad status codes
        response_json = response.json()
        
        text = f"Google Gemini AI response for Prompt: {prompt} \n *************************\n\n"
        if 'contents' in response_json and len(response_json['contents']) > 0:
            text += response_json['contents'][0]['parts'][0]['text']

        if not os.path.exists("GoogleGemini"):
            os.mkdir("GoogleGemini")

        with open(f"GoogleGemini/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"JSON decode error: {e}")
        print("Response content:", response.text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from SAM AI"
if __name__ == '__main__':
    print('Welcome to Sam A.I')
    say("sam A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "hi how are you".lower() in query:
            say(f"Hello ! good morning I'm fine excellencies. Hope you all are also doing good.")

        elif "music" in query:
            musicPath = r"C:\Users\user\Downloads\town-10169.mp3"
            os.startfile(musicPath)

        elif "what is the date today" in query:
            today = date.today()
            say(f"Sir, the date is {today}")
        
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {min} minutes")

        elif "create new word file".lower() in query.lower():
            os.startfile("C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE")

        elif "Sam quit".lower() in query.lower():
            exit()
        
        elif "creator info and current project".lower() in query:
            say(f"My creator is Nitya Agarwal, pursuing BTech and the current project she is making wonderful artificial intelligence!! me!!.")

        elif "reset chat".lower() in query.lower():
            chat_history = []
            say(f"Chat history has been cleared sir.")

        else:
            print("Chatting...")
            chat(query)