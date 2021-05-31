from flask import Flask, render_template, Response, jsonify
from flask import url_for
from pyngrok import ngrok
from ppt import *
import sys
name='test1'
count=-1
obj=''
title=''
app = Flask(__name__, static_url_path='/static')
public_url = ngrok.connect(port = '80')
print(public_url)
s=str(public_url)
abc=s.split(" ")
q=abc[1].replace('"',"")
q=q.replace('p','ps')
print(q)
@app.route('/')
def home():

   return render_template('home.html')

@app.route('/getfile')
def getfile():
    with open('file.txt', 'r') as f:
        transcript = f.read()
    return jsonify({'mystring':transcript})   

@app.route('/setfalse')
def setfalse():
    with open('file.txt', 'w') as f:
        f.write('false')
        f.close()
    return jsonify({'mystring':'done'}) 

@app.route('/mainhome')
def mainhome():


    return render_template('mainhome.html')

@app.route('/speech_to_text',methods=['GET', 'POST'])
def speech_to_text():
    # global count,q
    global count
    count=-1
    print(count)
    with open('transcript.txt', 'w') as f:
        f.truncate()
        f.close()
    user_input='What is the topic of your  powerpoint'
    talk(user_input) 
    print('jelo')

    return render_template('speech_to_text.html',data=q,data2=user_input,filename=name)

@app.route('/getaudio')    
def getaudio():
    
    with open('transcript.txt', 'r') as f:
        transcript = f.read()
    return jsonify({'mystring':transcript})  
    # return JsonResponse("someDictionary")

li=['Select the template by saying the number','what is your title ','do you have a subtitle','what is your subtitle','slide 1 done']
@app.route('/listen1')
def listen1():
    global count
    global li,obj,title
    count+=1  
    print(count)
    
    
    if count==0:
        data=listen()
        # add code to display templates 
        talk(li[count])
    if count==1:
        template={"1":'static/animals.pptx', "2":'static/business.pptx'}
        data=listen()
        # data=data.strip()
        dataarr=data.split()
        data=dataarr[1]
        print(data)
        if data in template:
            obj=CreatePpt(template[data])
            print('obj created')
            talk(li[count]) 
        else:
            talk('sorry template not available') 
            count=0
            return jsonify({'mystring':'sorry template not available'})   
            
           
            

    # if count==2:
    #     data=listen()
    #     talk(li[count])
        
    if count==2:       
        data=listen()
        
        obj.make_slide(0)
        title=data
        talk(li[count])
    if count==3:
        data=listen()
        print('title is',title)
        if 'yes' in data:
            talk(li[count])
        else:
            obj.ppt(title)    
        # os.startfile(fileName)
    if count==4:
        data=listen()
        obj.ppt(title,data)
        talk(li[count])
        # os.startfile(fileName)
    with open('file.txt','w') as f:
        f.write('True')
        f.close()
    # adsasd(data)
    return jsonify({'mystring':li[count]})

def adsasd(s):
    global li


if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")

    