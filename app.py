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

slide_layout=[]
i=0
n=0

def iterate():
    global i,n,slide_layout,count
    if i !=n:
        if 'Title' in slide_layout[i]:
            count=3           
        elif 'subtile' in slide_layout[i]:
            count=4  
        elif 'Text' in slide_layout[i]:
            count=5    
        talk(f'please enter T into {slide_layout[i]}')
        i+=1 
        return jsonify({'mystring':slide_layout[i-1]})
    else:
        count=1 
        talk('slide done,do you want to add more slides? ')
        return jsonify({'mystring':"slide done do you want to add more slides?"})
          



li=['Select the template by saying the number','do you have a new slide to add?','choose the layout','what is your title ',
'do you have a subtitle','what is your subtitle','slide 1 done']
@app.route('/listen1')
def listen1():
    global count
    global li,obj,title,slide_layout,i,n
    count+=1  
    print(count)
    
    
    if count==0:
        data=listen()
        # add code to display templates 
        talk(li[count])
        return jsonify({'mystring':li[count]})
    elif count==1:
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
            return jsonify({'mystring':li[count]})
        else:
            talk('sorry template not available') 
            count=0
            return jsonify({'mystring':'sorry template not available'})   
            
                       
    elif count==2:
        data=listen()
        if 'yes' in data:
            talk(li[count])
            return jsonify({'mystring':li[count]})
        else:
            count=7    

    elif count ==3:
        i=0
        data=listen()
        dic={"0":0,"1":1,"2":2}
        if data in dic:
            slide_layout=obj.make_slide(dic[data])
            print(slide_layout)
            n=len(slide_layout)
            return iterate()


    elif count==4:       
        data=listen()
        obj.add_title(data)
        # talk(f'please enter subtitle into {slide_layout[i]}')
        return iterate()
    elif count==5:
        data=listen()
        obj.add_subtitle(i-1,data)  # i-1 because i is incremented in iterate function
        return iterate() 
         
        # os.startfile(fileName)
    elif count==6:
        data=listen()
        # obj.ppt(title,data)
        talk(li[count])
        # os.startfile(fileName)
    elif count ==7:
        talk(li[count])

    elif count==8:
        talk('thank you')
        return jsonify({'mystring':"thank you"})

    with open('file.txt','w') as f:
        f.write('True')
        f.close()
    # adsasd(data)
    # return jsonify({'mystring':li[count]})

def adsasd(s):
    global li


if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")

    