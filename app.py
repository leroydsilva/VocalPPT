from flask import Flask, render_template, Response, jsonify,redirect,send_file,session,request,flash
from flask import url_for
import os, re, os.path
from ppt import talk,listen,CreatePpt
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
import psycopg2
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('AIzaSyCg_SQ6Lh-zZG1XyHPESnEz5iKEYsTQXJc', '1de73d9f58afbefc5')

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="postgres",
    dbpass="admin",
    dbhost="localhost",
    dbname="Vocal"
)

name='leroy'
count=-1
obj=''


app = Flask(__name__, static_url_path='/static')
Bootstrap(app)
app.config['SECRET_KEY'] = 'vocal'
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
conn = psycopg2.connect(host="localhost", port = 5432, database="Vocal", user="postgres", password="admin")
cur = conn.cursor()

# public_url = ngrok.connect(port = '80')
# print(public_url)
# s=str(public_url)
# abc=s.split(" ")
# q=abc[1].replace('"',"")
# q=q.replace('p','ps') 
# print(q)

class LoginForm(FlaskForm):
    phone = StringField('phone', validators=[InputRequired()],id='transcript')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    phone = StringField('phone', validators=[InputRequired(), Length(min=10)])

class User(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    phone = db.Column(db.String(80))

    def __init__(self, name=None, phone=None):
        self.name = name
        self.phone = phone

class Pictures(db.Model):
    pic_id = db.Column(db.Integer , primary_key=True)
    category = db.Column(db.String(100))
    path = db.Column(db.String(1000))

    def __init__(self, category=None, path=None):
        self.category = category
        self.path = path

class Templates(db.Model):
    t_id = db.Column(db.Integer , primary_key=True)
    category = db.Column(db.String(100))
    path = db.Column(db.String(1000))

    def __init__(self, category=None, path=None):
        self.category = category
        self.path = path

class Layouts(db.Model):
    l_id = db.Column(db.Integer , primary_key=True)
    category = db.Column(db.String(100))
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
    global name
    with open('transcript.txt', 'w') as f:
        f.truncate()
        f.close()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            if (user.phone, form.phone.data):
                # peter = User.query.filter_by(name=user.name).first()
                # name=peter.name
                session["phone"] = request.form.get("phone")
                # name=session["phone"]

                return redirect('mainhome')
        flash('Invalid Credentials')
    return render_template('login.html', form=form)

@app.route('/')
def home():

   return redirect('login')



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
    global count,cur
    count=-1
    print(count)
    with open('transcript.txt', 'w') as f:
        f.truncate()
        f.close()
    user_input='What is the topic of your  powerpoint'
    cur.execute("select category from templates group by category")
    # pic = Pictures.query.filter_by().first()
    rec_data=[]
    for x in cur.fetchall():
        print(x)
        rec_data.append(x[0])
    return render_template('mainhome.html',fname=user_input,data=rec_data)

@app.route('/speech_to_text',methods=['GET', 'POST'])
def speech_to_text():
    global count,name
    display()
    #talk(user_input) 
    print('jelo')
    

    return render_template('speech_to_text.html',ques=jugad,filename=name)




@app.route('/getaudio')    
def getaudio():
    
    with open('transcript.txt', 'r') as f:
        transcript = f.read()
    return jsonify({'mystring':transcript})  
    # return JsonResponse("someDictionary")

slide_layout=[]
pic_list=[]
pic_dir={}
i=0
n=0
query=picquery=chart_data=None
jugad=jugad1=None
def iterate():
    global i,n,slide_layout,count,jugad
    if i !=n:
        if 'Title' in slide_layout[i]:
            count=3          
        elif 'subtile' in slide_layout[i]:
            count=4  
        elif 'Text' in slide_layout[i]:
            count=5   
        elif 'Chart' in slide_layout[i]:
            count=9
            print('Chart')      
        elif 'Picture' in slide_layout[i]:
            count=7
            mypath = "static/pics"
            for root, dirs, files in os.walk(mypath):
                for file in files:
                    os.remove(os.path.join(root, file)) 
            talk('please enter the topic of the picture you want')
            i+=1 
            return jsonify({'mystring':"please enter the topic of the picture you want"})
        jugad=f'please enter data into {slide_layout[i]}'    
        talk(f'please enter data into {slide_layout[i]}')
        i+=1 
        return jsonify({'mystring':f'please enter data into {slide_layout[i-1]}'})
    else:
        count=1 
        jugad='slide done,do you want to add more slides?'
        talk('slide done,do you want to add more slides? ')
        return jsonify({'mystring':"slide done do you want to add more slides?"})
          

@app.route('/talkFunc/<strin>')    
def talkFunc(strin):
    talk(strin)
    return jsonify()

li=['Select the template by saying the number','choose the layout','choose the layout','',
]
@app.route('/listen1')
def listen1():
    global count
    global li,obj,slide_layout,i,n,query,picquery,pic_list,pic_dir,jugad1,chart_data
    count+=1  
    print(count)
    display()

    if count==0:
        topic=['science','business']
        data=listen()
        if 'audio' in data:
            count=-1  
            talk("Could not understand audio")
            return jsonify({'mystring':'Could not understand audio'})
        elif data in topic:
            query=data
            talk(li[count])    
            return jsonify({'mystring':li[count]})
        elif 'no topic' in data:
                obj=CreatePpt('static/0.pptx')
                count=2
                talk(li[count-1]) 
                return jsonify({'mystring':li[count-1]})
        
        
        talk(li[count])    
        return jsonify({'mystring':li[count]})

    elif count==1:
        template={"1":'static/Business_1.pptx', "2":'static/Business_2.pptx',"3":"static/Science_1.pptx","4":"static/Science_2.pptx"}
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
            count=2
            talk(li[count-1]) 
            
            return jsonify({'mystring':li[count-1]})
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
            print('thanks')
            return redirect('/')  
        else:
            talk('sorry did not get you') 
            count=1
            return jsonify({'mystring':'sorry did not get you'})     

    elif count==3:
        i=0
        data=listen()
        dic={"0":0,"1":1,"2":2,"3":3,"4":4,"5":5}
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
            data=listen()
            if data=='Could not understand audio':
                count=7  
                talk("Could not understand audio")
                return jsonify({'mystring':'Could not understand audio'})
            else:
                picquery=data
                gis.search(search_params={'q': picquery,'num': 5, 'safe': 'medium','fileType': 'jpg,gif,png','imgType': 'photo'}, path_to_dir='static/pics',custom_image_name='pic')
                pic_list=os.listdir('static/pics')
                pic_dir = {str(i): f'static/pics/{pic_list[i]}' for i in range(0, len(pic_list))}
                print(pic_dir)
                jugad1='choose the Picture by saying the number'
                talk("choose the Picture by saying the number")
                return jsonify({'mystring':'choose the Picture by saying the number'})



    elif count ==9:
        # images={"1":'static/1.jpg', "2":'static/2.jpg'}

        data=listen()
        dataarr=data.split()
        data=dataarr[1]
        if data in pic_dir:
            obj.add_image(i-1,pic_dir[data])
            display()
            return iterate()    
        else:
            talk('Picture not available') 
            count=8
            return jsonify({'mystring':'Picture not available'})

    elif count==10:
        data=listen()
        chart_data=data.split()
        talk('enter the Y values') 
        return jsonify({'mystring':'enter the Y values'})
    elif count==11:
        data=listen()
        num_data=data.split()
        obj.add_chart(chart_data,num_data,i-1)
        return iterate()



def display():
    with open('file.txt','w') as f:
        f.write('True')
        f.close()


@app.route('/template')
def template():
    global count,li,query,cur
    if query!=None:
        cur.execute(f"select t_id,path from templates where category='{query}'")
    else:
        cur.execute("select t_id,path from templates")    
    # pic = Pictures.query.filter_by().first()
    rec_data=[]
    # num=[]
    for x in cur.fetchall():
        print(x)
        # num.append(x[0])
        rec_data.append(x[1])
    return render_template('tempDisplay.html',data=rec_data,q=li[count])

@app.route('/layout')
def layout():
    global count,li,query,cur
    cur.execute("select path from layouts order by l_id")
    # pic = Pictures.query.filter_by().first()
    rec_data=[]
    for x in cur.fetchall():
        print(x)
        rec_data.append(x[0])
    return render_template('layoutDisplay.html',data=rec_data,q=li[count])

@app.route('/picture')
def picture():
    global count,li,query,cur,pic_list
    
    return render_template('picDisplay.html',data=pic_list,q=jugad1)

# @app.route('/download')
# def download():
#     global name
#     #For windows you need to use drive name [ex: F:/Example.pdf]
#     path = f"static/{name}.pptx"
#     return send_file(path, as_attachment=True)

@app.route('/hello')
def hello():
    global count,name
    
    #talk(user_input) 
    print('jelo')
    

    return render_template('hello.html',ques=li[count],filename=name)




@app.route("/logout")
def logout():
    session["phone"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")

    