import pyttsx3
from decouple import config
import speech_recognition as sr
from random import choice
from utils import opening_text
import requests
import pyaudio

from functions.online_ops import ip, advice, news, jokes, movies, climate, email, whatsapp, google, youtube, wiki
from functions.os_ops import camera, notepad, discord, cmd, calc

from pprint import pprint
from datetime import datetime

USERNAME = config("USER")
BOTNAME = config("BOTNAME")

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 100)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.stop()
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 16:
        speak("Good afternoon sir")
    elif 16 <= hour < 20:
        speak("Good evening sir")
    else:
        speak("Hello sir")

    speak("How may I assist you today?")

def user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')

        if "exit" in query or "stop" in query:
            hour = datetime.now().hour
            if 23 <= hour or hour < 6:
                speak("Good night sir")
            else:
                speak("Have a good day sir")
            exit()

        speak(choice(opening_text))
        return query

    except Exception:
        speak("Could you please say that again?")
        return ""

if __name__ == '__main__':
    greet()

    while True:
        query = user_input().lower()

        if "open notepad" in query:
            notepad()

        elif "open discord" in query:
            discord()

        elif "open cmd" in query or "open command prompt" in query:
            cmd()

        elif "open camera" in query:
            camera()

        elif "open calculator" in query:
            calc()

        elif "ip address" in query:
            ip_address = ip()
            speak(f"Your IP is {ip_address}. It is printed on the screen sir")
            print(f"Your IP is {ip_address}")

        elif "wikipedia" in query:
            speak("What do you want to search in Wikipedia sir?")
            search_query = user_input().lower()
            results = wiki(search_query)
            speak(f"According to Wikipedia, {results}")
            print(results)

        elif "youtube" in query:
            speak("What do you want to play on YouTube sir?")
            video = user_input().lower()
            youtube(video)

        elif "google search" in query or "search on google" in query:
            speak("What do you want to search on Google sir?")
            gq = user_input().lower()
            google(gq)

        elif "message" in query or "whatsapp" in query:
            speak("On what number should I send the message sir? Please enter it in the console")
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = user_input().lower()
            whatsapp(number, message)
            speak("Message sent successfully sir")

        elif "send a mail" in query or "email" in query:
            speak("Who should I send the mail to sir?")
            receiver = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = user_input().capitalize()
            speak("What is the message sir?")
            msg = user_input().capitalize()

            if email(receiver, subject, msg):
                speak("Email has been sent successfully sir")
            else:
                speak("Something went wrong. Please check the error logs sir")

        elif "joke" in query:
            joke = jokes()
            speak("Hope you like this sir")
            speak(joke)
            pprint(joke)

        elif "advice" in query:
            guidance = advice()
            speak("Here's an advice for you sir")
            speak(guidance)
            pprint(guidance)

        elif "trending movies" in query:
            mv = movies()
            speak("Some of the trending movies are on your screen sir")
            print(*mv, sep="\n")

        elif "news" in query:
            ns = news()
            speak("Here is the latest news sir")
            print(*ns, sep="\n")

        elif "weather" in query:
            address = ip()
            city = requests.get(f"https://ipapi.co/{address}/city/").text
            speak(f"Getting weather for your city {city}")
            weather_desc, temperature, feels_like = climate(city)

            speak(f"The temperature is {temperature}°C but feels like {feels_like}°C")
            speak(f"The weather report says {weather_desc}")

            print(f"Description: {weather_desc}\nTemperature: {temperature}\nFeels like: {feels_like}")

        else:
            speak("I did not understand that sir. Please say it again.")
