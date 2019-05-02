import os
import webbrowser
import speech_recognition as sr
from gtts import gTTS
from time import ctime
import time
import subprocess
import sys

def speak(audioString):
	#playaudio
	print(audioString)
	tts = gTTS(text=audioString, lang='en')
	tts.save("hello.mp3")
	os.system("mpg321 hello.mp3")

def recordAudio():
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	try:
		data = r.recognize_google(audio)
		return data
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
def jarvis(data):
	if(data=="how are you"):
		speak("I am fine")
	if "what time is it" in data:
		speak(ctime())
	if "where is" in data:
		data = data.split(" ")
		location = data[2]
		speak("Hold on Frank, I will show you where " + location + " is.")
		webbrowser.open('https://www.google.nl/maps/place/' + location + "/&amp;")
	if(data=="exit"):
		speak("exiting")
		sys.exit()
	if(data=="shutdown"):
		speak("do you want to shutdown now")
		data = recordAudio()
		if(data=="yes"):
			speak("system is shutting down")
			os.system("init 0")
	if(data=="restart"):
		speak("do you want to restart now")
		data = recordAudio()
		if(data=="yes"):
			speak("system is restarting")
			os.system("init 6")
	if(data=="web browser"):
		speak("opening browser")
		webbrowser.open('http://www.google.com')
	if(data=="text editor"):
		speak("openng text editor")
		proc = subprocess.Popen(['gedit', 'file.txt'])
	if(data=="search"):
		speak("what do you want to search")
		data=recordAudio()
		webbrowser.open("https://www.google.com/search?client=ubuntu&channel=fs&q="+text)
	if(data=="about"):
		os.system("gnome-control-center info-overview")
	if(data=="python"):
		os.system("/usr/bin/python3.6")
	if(data=="sub lime"):
		os.system("/opt/sublime_text/sublime_text %F")
	if(data=="VLC"):
		os.system("/usr/bin/vlc --started-from-file %U")
	if(data=="camara"):
		os.system("cheese")
	if(data=="sudoku"):
		os.system("gnome-sudoku")


			


time.sleep(2)
speak("Hi Frank, what can I do for you?")
while 1:
	data = recordAudio()
	jarvis(data)
