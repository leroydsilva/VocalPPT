from pptx import Presentation
import pyttsx3
import speech_recognition as sr
from app import name

def talk(audio):
    
    # time.sleep(2)
    # if audio==None:
    #     engine.say('good morning')
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[0])
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)
    engine.say(audio)
    engine.runAndWait()
    return 

def listen():
    

    # get audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        # r.pause_threshold=1
        # r.energy_threshold=200
        print("Speak:")
        audio = r.listen(source)

    try:
        output = "" + r.recognize_google(audio)
    except sr.UnknownValueError:
        output = "Could not understand audio"
    except sr.RequestError as e:
        output = "Could not request results; {0}".format(e)

    data =output
    with open('transcript.txt', 'w') as f:
        f.write(data)
        f.close()
    return data.lower()

class CreatePpt:
    # global fileName
    def __init__(self,temp=None):
         self.pr1=Presentation(temp)         

    def ppt(self,title,subtitle=""):    
        self.title1=self.slide.shapes.title
        self.title1.text=title
        self.pr1.save("static/{}.pptx".format(name))
        self.subtitle1=self.slide.placeholders[1]
        self.subtitle1.text=subtitle
        self.pr1.save("static/{}.pptx".format(name))
        print('done sucessfully')

    def make_slide(self,layout):
        self.slide=self.pr1.slides.add_slide(self.pr1.slide_layouts[layout])
        
