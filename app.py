from flask import Flask, render_template, Response, jsonify,redirect
from flask import url_for
from pyngrok import ngrok
from ppt import talk,listen,CreatePpt
import sys
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
import psycopg2

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="postgres",
    dbpass="admin",
    dbhost="localhost",
    dbname="Vocal"
)

name='test1'
count=-1
obj=''
title=''

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)
app.config['SECRET_KEY'] = 'vocal'
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

public_url = ngrok.connect(port = '80')
print(public_url)
s=str(public_url)
abc=s.split(" ")
q=abc[1].replace('"',"")
q=q.replace('p','ps')
print(q)

class LoginForm(FlaskForm):
    phone = StringField('phone', validators=[InputRequired()],id='transcript')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    phone = StringField('phone', validators=[InputRequired(), Length(max=10)])

class User(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    phone = db.Column(db.String(80))

    def __init__(self, name=None, phone=None):
        self.name = name
        self.phone = phone

class Pictures(db.Model):
    category = db.Column(db.String(100), primary_key=True)
    path = db.Column(db.String(1000))

    def __init__(self, category=None, path=None):
        self.category = category
        self.path = path


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        
        new_user = User(name=form.username.data, phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user created</h1>'
    return render_template('signup.html', form=form)

# @app.route('/getaudiologin')    
# def getaudiologin():
    
#     with open('login_transcript.txt', 'r') as f:
#         transcript = f.read()
#     return jsonify({'mystring':transcript}) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    with open('transcript.txt', 'w') as f:
        f.truncate()
        f.close()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            if (user.phone, form.phone.data):
                

                return redirect('speech_to_text')
        return 'Invalid Phone Number'
    return render_template('login.html', form=form)

@app.route('/')
def home():

   return render_template('index.html')

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
    conn = psycopg2.connect(host="localhost", port = 5432, database="Vocal", user="postgres", password="admin")
    cur = conn.cursor()
    cur.execute("SELECT path FROM Pictures")
    # pic = Pictures.query.filter_by().first()
    print(cur)
    rec_data=[]
    for x in cur.fetchall():
        print(x)
        rec_data.append(x[0])

    return render_template('mainhome.html',data=rec_data)

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
    #talk(user_input) 
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
            print('title')         
        elif 'subtile' in slide_layout[i]:
            count=4  
            print('subtitle')
        elif 'Text' in slide_layout[i]:
            count=5 
            print('text')   
        elif 'Picture' in slide_layout[i]:
            count=7 
            print('Picture')    
        talk(f'please enter data into {slide_layout[i]}')
        i+=1 
        return jsonify({'mystring':f'please enter data into {slide_layout[i]}'})
    else:
        count=1 
        talk('slide done,do you want to add more slides? ')
        return jsonify({'mystring':"slide done do you want to add more slides?"})
          

@app.route('/talkFunc/<strin>')    
def talkFunc(strin):
    talk(strin)
    return jsonify()

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
        dataarr=data.split()
        try:
            data=dataarr[1]
        except:
            data=dataarr[0]    
        print(data)
        if data in template:
            obj=CreatePpt(template[data])
            display()
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
        elif 'no' in data:
            count=9    
        else:
            talk('sorry did not get you') 
            count=1
            return jsonify({'mystring':'sorry did not get you'})     

    elif count ==3:
        i=0
        data=listen()
        dic={"0":0,"1":1,"2":2}
        dataarr=data.split()
        try:
            data=dataarr[1]
        except:
            data=dataarr[0] 
        if data in dic:
            slide_layout=obj.make_slide(dic[data])
            display()
            print(slide_layout)
            n=len(slide_layout)
            return iterate()
        else:
            talk('layout not available') 
            count=2
            return jsonify({'mystring':'layout not available'})

    elif count==4:       
        data=listen()
        obj.add_title(data)
        display()
        return iterate()
    elif count==5:
        data=listen()
        print('subtitle')
        obj.add_subtitle(i-1,data)  # i-1 because i is incremented in iterate function
        display()
        return iterate() 
         
        
    elif count==6:
        data=listen()
        obj.add_text(i-1,data)
        display()
        talk('Do you have more text to add') 
        return jsonify({'mystring':'Do you have more text to add'})
    elif count==7:
        data=listen()
        if 'yes' in data:
            count=5
            talk('next point?') 
            return jsonify({'mystring':'next point?'})
        elif 'no' in data:
            return iterate()    
        else:
            talk('sorry did not get you') 
            count=6
            return jsonify({'mystring':'sorry did not get you'})    
        
    elif count ==8:
        images={"1":'static/1.jpg', "2":'static/2.jpg'}
        data=listen()
        # data=data.strip()
        dataarr=data.split()
        data=dataarr[1]
        if data in images:
            obj.add_image(i-1,images[data])
            display()
            return iterate()    
        else:
            talk('Picture not available') 
            count=7
            return jsonify({'mystring':'Picture not available'})    

    elif count ==9:
        talk(li[count])

    elif count==10:
        talk('thank you')
        return jsonify({'mystring':"thank you"})



def display():
    with open('file.txt','w') as f:
        f.write('True')
        f.close()


if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")

    