from pptx import Presentation
import pyttsx3
import speech_recognition as sr
from pptx.util import Inches
from PIL import Image
import os
from flask import session
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
name='leroy'
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
        # r.energy_threshold=300
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
    global name
    def __init__(self,temp=None):
         self.pr1=Presentation(temp) 
        #  name=session['phone']
        #  print(name+'thsi is naem asdorekokeo')
        #  self.pr1.save("static/{}.pptx".format(name)) 

    def make_slide(self,layout):
        self.slide=self.pr1.slides.add_slide(self.pr1.slide_layouts[layout])
        self.pr1.save("static/{}.pptx".format(name))
        os.system(f'ppt2pdf file static/{name}.pptx')
        print('done')
        self.l=[]
        self.ph=[]
        for s in self.slide.placeholders:
                self.l.append(s.name)
                self.ph.append(s.placeholder_format.idx)

        return self.l            

    def add_title(self,title):
        self.title1=self.slide.shapes.title
        self.title1.text=title
        self.pr1.save("static/{}.pptx".format(name))
        os.system(f'ppt2pdf file static/{name}.pptx')
        


    def add_subtitle(self,ph_num,subtitle=""):    
        self.subtitle1=self.slide.placeholders[self.ph[ph_num]]
        self.subtitle1.text=subtitle
        self.pr1.save("static/{}.pptx".format(name))
        os.system(f'ppt2pdf file static/{name}.pptx')
        print('done sucessfully')

    def add_text(self,ph_num,text_data=""):
        self.t=self.slide.placeholders[self.ph[ph_num]]
        self.text_frame = self.t.text_frame
        self.p=self.text_frame.add_paragraph()
        self.run = self.p.add_run()
        self.run.text=text_data
        self.pr1.save("static/{}.pptx".format(name))
        os.system(f'ppt2pdf file static/{name}.pptx')
        print("done text")

    def add_chart(self,data,num_data,ph_num):
        self.t=self.slide.placeholders[self.ph[ph_num]]
        self.chart_data = CategoryChartData()
        self.chart_data.categories = data
        self.num_arr=[int(x) for x in num_data]
        self.chart_data.add_series('Series 1', self.num_arr)
        self.t = self.t.insert_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,self.chart_data)
        self.pr1.save("static/{}.pptx".format(name))
        print('done chart...................')
        os.system(f'ppt2pdf file static/{name}.pptx')



    def add_image(self, ph_num, image_url):
        self.placeholder = self.slide.placeholders[self.ph[ph_num]]

        # Calculate the image size of the image
        im = Image.open(image_url)
        width, height = im.size

        # Make sure the placeholder doesn't zoom in
        self.placeholder.height = height
        self.placeholder.width = width

        # Insert the picture
        self.placeholder = self.placeholder.insert_picture(image_url)

        # Calculate ratios and compare
        image_ratio = width / height
        self.placeholder_ratio = self.placeholder.width / self.placeholder.height
        ratio_difference = self.placeholder_ratio - image_ratio

        # Placeholder width too wide:
        if ratio_difference > 0:
            difference_on_each_side = ratio_difference / 2
            self.placeholder.crop_left = -difference_on_each_side
            self.placeholder.crop_right = -difference_on_each_side
        # Placeholder height too high
        else:
            difference_on_each_side = -ratio_difference / 2
            self.placeholder.crop_bottom = -difference_on_each_side
            self.placeholder.crop_top = -difference_on_each_side
        self.pr1.save("static/{}.pptx".format(name))
        os.system(f'ppt2pdf file static/{name}.pptx')

    
        
