import pyttsx3

engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
engine.setProperty('rate', 120)
engine.say('Hello master')
engine.setProperty('rate', 100)
engine.say("Do you need something?")

engine.runAndWait()

engine.setProperty('rate', 100)
engine.say("Do you need something?")

engine.runAndWait()