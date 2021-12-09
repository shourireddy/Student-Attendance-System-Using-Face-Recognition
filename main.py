from flask import Flask,render_template,request,redirect,url_for,Response,current_app,session,flash,jsonify
from flaskext.mysql import MySQL
from functools import wraps
from flask_mail import Mail, Message
from threading import Timer
#from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from werkzeug.test import EnvironBuilder
from datetime import datetime
from datetime import timedelta
import cv2
import json
import math
import copy
import numpy as np
import sys
import time
import os
from os.path import isdir, join, isfile, splitext
from os import listdir
app=Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!@#$'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
mail = Mail(app)
mysql=MySQL(app)
mail.init_app(app)
# Configuring E-Mail
app.config.update(
    DEBUG = False,
    #Email settings
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'vineethreddypachika@gmail.com',
    MAIL_PASSWORD = 'vinnuvishal',
    MAIL_DEFAULT_SENDER = ('KITSW','vineethreddypachika@gmail.com')
    )
mail = Mail(app)

# Database Connection
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='multiuser'

#Protected page for home through login_required
def login_requiredadmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_inadmin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def login_requiredstudent(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_instudent' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def login_requiredlecturer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_inlecturer' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# User login Middleware code
@app.route('/login',methods=['GET','POST'])    
def login():
    if request.method=='POST':
        global username
        username=request.form['username']
        password=request.form['password']
        usertype=request.form['usertype']
        connection=mysql.connect()
        cur=connection.cursor()
        cur.execute("SELECT * FROM "+usertype+" WHERE Username='"+username+"' and Password='"+password+"' and Usertype='"+usertype+"'")
        data=cur.fetchone()
        if data is None:
            return render_template("login.html",msg="Input Credentials are Wrong")
        elif usertype=="Administrator":
            session['logged_inadmin']=True
            session['username']=username
            return redirect(url_for('adminhome'))
        elif usertype=="Student":
            session['logged_instudent']=True
            session['username']=username
            return redirect(url_for('studenthome'))
        elif usertype=="Lecturer":
            session['logged_inlecturer']=True
            session['username']=username
            return redirect(url_for('lecturerhome'))
    return render_template("login.html")
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Forgotpassword Middleware code
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST':
        username=request.form['username']
        usertype=request.form['usertype']
        connection=mysql.connect()
        cur=connection.cursor()
        cur.execute("SELECT Password,Emailid,Fullname FROM "+usertype+" WHERE Username='"+username+"' and Usertype='"+usertype+"'")
        data=cur.fetchone()
        if data is None:
            return render_template("forgotpassword.html",msg1=username,msg2=" account not found")
        else:
            msg = Message('Forgot Password?',recipients= [data[1]])
            msg.body = "Hi " + data[2] + " your account password is '" + data[0] + "'"
            msg.html = "<p><b>Dear " + data[2] + ",</b></p><p>Your Face Recognition Student Attendance System account password is <b>" + data[0] + "</b></p>"
            mail.send(msg)
            return render_template("forgotpassword.html",msg1="Your password has been sent to ",msg2=data[1])
    return render_template("forgotpassword.html")
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# User registration Middleware code 
@app.route('/adminhome/register',methods=['GET','POST'])
# @login_requiredadmin
def register():
    if request.method=='POST':
        usertype=request.form['usertype']
        if usertype=="Student":
            username=request.form['rollno']
            section=request.form['section']
            fullname=request.form['name']
            emailid=request.form['email']
            pemailid=request.form['parentemail']
            mobileno=request.form['mnumber']
            password=request.form['password']
            #encryptpass=generate_password_hash(password,method='sha256')
            connection=mysql.connect()
            cur=connection.cursor() 
            cur.execute("INSERT INTO student (Usertype,Username,Section,Fullname,Emailid,ParentsEmailid,Mobilenumber,Password,Course,Attendance,DateandTime,AttPercentage) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(usertype,username,section,fullname,emailid,pemailid,mobileno,password,'','','',''))
            connection.commit()
            return render_template("register.html",msg1="***",usname=username,msg2=" Registered Successfully***") 
        elif usertype=="Lecturer":
            uname=request.form['uname']
            fullname=request.form['name']
            emailid=request.form['email']
            mobileno=request.form['mnumber']
            password=request.form['password']
            #encryptpass=generate_password_hash(password,method='sha256')
            connection=mysql.connect()
            cur=connection.cursor()
            cur.execute("INSERT INTO lecturer (Usertype,Username,Fullname,Emailid,Mobilenumber,Password,AllottedCourse,AllottedSection) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(usertype,uname,fullname,emailid,mobileno,password,'',''))
            connection.commit()
            return render_template("register.html",msg1="***",usname=uname,msg2=" Registered Successfully***")
    return render_template("register.html")

#face registration and function
@app.route('/faceregister',methods=['GET','POST'])
def faceregister():
    if request.method=='POST':
        global section,rollno
        section=request.form['section2']
        rollno=request.form['rollno2']
        connection=mysql.connect()
        cur=connection.cursor()
        cur.execute("SELECT * FROM student WHERE Username='"+rollno+"' and Section='"+section+"'")
        data=cur.fetchone()
        if data is None:
            return render_template("register.html",message="First,Register in the above form")
        else:
            section=data[2]
            rollno=data[1]
            print(section,rollno)
            return render_template("register.html",message="***"+rollno+" Face Registered Successfully***")
    return render_template("register.html")

#Creating DataSet
def get_frame():
    with app.test_request_context():
        faceregister()
        studenthome()
    global rollnoshort
    rollnoshort=str(rollno[1:3])+str(rollno[-3:])
    camera_port=cv2.CAP_DSHOW     
    ramp_frames=100
    facecascade=cv2.CascadeClassifier('Classifier/haarcascade_frontalface_default.xml')
    camera=cv2.VideoCapture(camera_port)#this makes a web cam object
    camera.set(5,60)
    i=1
    count=0;
    while True:
        ret,img = camera.read()
        img = cv2.flip(img, 1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=facecascade.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            train=os.path.join(APP_ROOT,"Face Datasets/")
            if not os.path.isdir(train):
                os.mkdir(train)
            directory=os.path.join(APP_ROOT,"Face Datasets/"+section+"/")
            if not os.path.isdir(directory):
                os.mkdir(directory)
            directory1=os.path.join(APP_ROOT,"Face Datasets/"+section+"/"+rollno+"/")
            if not os.path.isdir(directory1):
                os.mkdir(directory1)
            count=count+1
            cv2.imwrite("Face Datasets/"+section+"/"+rollno+"/"+rollnoshort+"_"+str(count)+".jpg",cv2.resize(gray[y:y+h,x:x+w],(300,300)))
            cv2.rectangle(img,(x,y),(x+w,y+h),(75,238,255),2)
        cv2.waitKey(100)
        if count>49:
            break
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
    camera.release()
    del(camera)
    cv2.destroyAllWindows()
    def Addrollno():
        Info = open("Rollno's.txt", "a+")
        ID=rollnoshort
        Info.write(str(ID) + "," + rollno + "\n")
        print ("Rollno Stored in " + str(ID))
        Info.close()
        return ID
    Addrollno()
    return trainner()

#Creating Trained data file
def trainner():
    recognizer=cv2.face.EigenFaceRecognizer_create()
    detector= cv2.CascadeClassifier("Classifier/haarcascade_frontalface_default.xml")
    path=os.path.join(APP_ROOT,"Face Datasets")
    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in listdir(path)]
        #create empty face list
        faceSamples=[]
        #create empty ID list
        rollnos=[]
        #now looping through all the image paths and loading the Ids and the images
        for root,dirs,imagePaths in os.walk(path):
            for imagePath in imagePaths:
                # Updates in Code
                # ignore if the file does not have jpg extension :
                if(os.path.split(imagePath)[-1].split(".")[-1]!='jpg'):
                    continue
                #dir to image path
                imagePath=os.path.join(root,imagePath)
                #loading the image and converting it to gray scale
                FaceImage=Image.open(imagePath).convert('L')
                FaceImage=FaceImage.resize((300,300))
                #Now we are converting the PIL image into numpy array
                imageNp=np.array(FaceImage,'uint8')
                #getting the Id from the image
                rollno=int(os.path.split(imagePath)[-1].split('_')[0])
                faces = detector.detectMultiScale(imageNp)
                for (x,y,w,h) in faces:
                    faceSamples.append(cv2.resize(imageNp[y:y+h,x:x+w],(300,300)))
                    rollnos.append(rollno)
                    cv2.waitKey(10)
        return faceSamples,rollnos
    faces,rollnos=getImagesAndLabels(path)
    recognizer.train(faces,np.array(rollnos))
    recognizer.write('Training Data/trainingDataEigen.yml')
    print("\n[INFO] {0} faces trained. Exiting Program".format(len(np.unique(rollnos))))
    

@app.route('/webcam')
def webcam():
    global start
    start = time.time()
    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

#adminhome dashboard
@app.route('/adminhome',methods=['GET','POST'])
@login_requiredadmin
def adminhome():
    global section,course,lecturers,sections,lecallotdata,rollnoatt,startdatetime
    rollnoatt = []
    startdatetime=datetime.now().strftime('%Y-%m-%d %I:%M %p')
    connection=mysql.connect()
    cur=connection.cursor()
    cur.execute("SELECT Usertype FROM Administrator")
    data=cur.fetchone()
    cur.execute("SELECT Fullname FROM lecturer")
    lecdata=cur.fetchall()
    cur.execute("SELECT DISTINCT Section FROM student")
    secdata=cur.fetchall()
    cur.execute("SELECT Username,Fullname,AllottedCourse,AllottedSection FROM lecturer")
    allotdata=cur.fetchall()
    if request.method=='POST':
        lecturer=request.form['lecturer']
        section=request.form['section']
        course=request.form['course']
        if request.form.get('submit')=='Submit':
            cur.execute("SELECT Username,Section,Emailid,ParentsEmailid,Mobilenumber,AttPercentage FROM student where Section='"+section+"' ORDER BY Username ASC")
            studdata=cur.fetchall()
            cur.execute("SELECT Username FROM student where Section='"+section+"' ORDER BY Username ASC")
            rolldata=cur.fetchall()
            cur.execute("SELECT AttPercentage FROM student where Section='"+section+"' ORDER BY Username ASC")
            attdataf=cur.fetchall()
            attdata = []
            for row in attdataf:
                row=str(row[0])
                row=str(row[0:4])
                attdata.append(row)
            return render_template("adminhome.html",mesg1=data[0],lecturers=lecdata,sections=secdata,lecallotdata=allotdata,studdata=studdata,rolldata=rolldata,attdata=attdata)
        else:
            connection=mysql.connect()
            cur=connection.cursor()
            cur.execute("UPDATE lecturer SET AllottedCourse='"+course+"',AllottedSection='"+section+"' where Fullname='"+lecturer+"'")
            connection.commit()
            cur.execute("SELECT Username,Fullname,AllottedCourse,AllottedSection FROM lecturer")
            allotdata=cur.fetchall()
            return render_template("adminhome.html",mesg1=data[0],lecturers=lecdata,sections=secdata,lecallotdata=allotdata,mesg="Section and Course Allotted Successfully to "+lecturer)
    return render_template("adminhome.html",mesg1=data[0],lecturers=lecdata,sections=secdata,lecallotdata=allotdata)

#studenthome dashboard
@app.route('/studenthome',methods=['GET','POST'])
@login_requiredstudent
def studenthome():
    global attper,totalclasses,presentclasses,courses,subjects,classesnum
    with app.test_request_context():
        login()
    connection=mysql.connect()
    cur=connection.cursor()
    cur.execute("SELECT * FROM student where Username='"+username+"'")
    data=cur.fetchone()
    global section,rollno
    section=data[2]
    rollno=data[1]
    if request.method=='POST':
        emailid=request.form['email']
        mobileno=request.form['mnumber']
        connection=mysql.connect()
        cur=connection.cursor()
        cur.execute("UPDATE student SET Emailid='"+emailid+"',Mobilenumber='"+mobileno+"' where Username='"+username+"'")
        connection.commit()
        return render_template("studenthome.html",mesg1=data[3],output1=attper,output2=totalclasses,output3=presentclasses,courses=courses,subjects=subjects,classesnum=classesnum,input1=data[3],input2=data[1],input3=data[2],input4=data[5],input5=emailid,input6=mobileno,fmesg="Email ID and Mobile No. Updated Successfully") 
    cur.execute("SELECT count(Course) from attendance where Section='"+section+"' and Username='"+rollno+"'")
    totalclasses=cur.fetchone()
    totalclasses=int(totalclasses[0])
    cur.execute("SELECT count(Attendance) from attendance where Section='"+section+"' and Username='"+rollno+"' and Attendance='Present'")
    presentclasses=cur.fetchone()
    presentclasses=int(presentclasses[0])
    if (totalclasses==presentclasses==0):
        Percentage="0.0"
    else:
        Percentage=float((presentclasses/totalclasses)*100)
        Percentage=str("{0:.1f}%".format(Percentage))
    cur.execute("SELECT AttPercentage FROM student where Username='"+rollno+"' and Section='"+section+"'")
    attper=cur.fetchone()
    attper=attper[0]
    cur.execute("SELECT Course,StartPeriodTime,EndPeriodTime FROM attendance where Username='"+rollno+"' and Section='"+section+"' and Attendance='Absent' ORDER BY StartPeriodTime DESC")
    courses=cur.fetchall()
    cur.execute("SELECT DISTINCT Course FROM attendance where Username='"+rollno+"' and Section='"+section+"'")
    datasec=cur.fetchall()
    subjects = []
    classesnum = []
    for row in datasec:
        cur.execute("SELECT count(Course),Course FROM attendance where Section='"+section+"' and Course='"+str(row[0])+"' and Username='"+rollno+"'")
        coursenum=cur.fetchone()
        coursenum=str(coursenum[0])
        row1=str(row[0]+"("+coursenum+")")
        subjects.append(row1)
        cur.execute("SELECT count(Attendance) FROM attendance where Username='"+rollno+"' and Section='"+section+"' and Course='"+str(row[0])+"' and Attendance='Present'")
        num=cur.fetchone()
        num=str(num[0])
        classesnum.append(num)
    return render_template("studenthome.html",mesg1=data[3],output1=attper,output2=totalclasses,output3=presentclasses,courses=courses,subjects=subjects,classesnum=classesnum,input1=data[3],input2=data[1],input3=data[2],input4=data[5],input5=data[4],input6=data[6])

#lecturerhome dashboard
@app.route('/lecturerhome',methods=['GET','POST'])
@login_requiredlecturer
def lecturerhome():
    with app.test_request_context():
        login()
    connection=mysql.connect()
    cur=connection.cursor()
    cur.execute("SELECT * FROM lecturer where Username='"+username+"'")
    data=cur.fetchone()
    cur.execute("SELECT count(Username) FROM student where Section='"+data[8]+"'")
    stud=cur.fetchone()
    cur.execute("SELECT count(DISTINCT StartPeriodTime) FROM attendance where Section='"+data[8]+"' and Course='"+data[7]+"'")
    tclasses=cur.fetchone()
    cur.execute("SELECT DISTINCT Username,Section,Course FROM attendance where Section='"+data[8]+"' and Course='"+data[7]+"' ORDER BY Username ASC")
    table=cur.fetchall()
    cur.execute("SELECT * FROM attendance where Section='"+data[8]+"' and Course='"+data[7]+"' ORDER BY Username ASC,StartPeriodTime DESC")
    totalatt=cur.fetchall()
    pemailid = []
    mobno = []
    presents = []
    absents = []
    for row in table:
        cur.execute("SELECT ParentsEmailid,Mobilenumber FROM student where Section='"+data[8]+"' and Username='"+row[0]+"' ORDER BY Username ASC")
        pinfo=cur.fetchall()
        cur.execute("SELECT count(Attendance) FROM attendance where Section='"+data[8]+"' and Course='"+data[7]+"'and Username='"+row[0]+"'and Attendance='Present' ORDER BY Username ASC")
        present=cur.fetchone()
        cur.execute("SELECT count(Attendance) FROM attendance where Section='"+data[8]+"' and Course='"+data[7]+"'and Username='"+row[0]+"'and Attendance='Absent' ORDER BY Username ASC")
        absent=cur.fetchone()
        for row in pinfo:
            pmail=str(row[0])
            mno=str(row[1])
            pemailid.append(pmail)
            mobno.append(mno)
        for row in present:
            row=str(row)
            presents.append(row)
        for row in absent:
            row=str(row)
            absents.append(row)
    output=list(zip(table,pemailid,mobno,presents,absents))
    if request.method=='POST':
        emailid=request.form['email']
        mobileno=request.form['mnumber']
        connection=mysql.connect()
        cur=connection.cursor()
        cur.execute("UPDATE lecturer SET Emailid='"+emailid+"',Mobilenumber='"+mobileno+"' where Username='"+username+"'")
        connection.commit()
        return render_template("lecturerhome.html",mesg1=data[3],input1=data[3],input2=data[2],input3=emailid,input4=mobileno,fmesg="Email ID and Mobile No. Updated Successfully",output11=data[8],output12=data[7],output13=stud[0],output14=tclasses[0],students=table,emailid=pemailid,mnumber=mobno,stuatt=totalatt,bar1=presents,bar2=absents,htmltable=output)
    return render_template("lecturerhome.html",mesg1=data[3],input1=data[3],input2=data[2],input3=data[4],input4=data[5],output11=data[8],output12=data[7],output13=stud[0],output14=tclasses[0],students=table,emailid=pemailid,mnumber=mobno,stuatt=totalatt,bar1=presents,bar2=absents,htmltable=output)

#logout from dashboard
@app.route('/logoutadmin')
@login_requiredadmin
def logoutadmin():
    session.clear()
    return render_template("login.html",msg="You have been logged out!!!")

@app.route('/logoutstudent')
@login_requiredstudent
def logoutstudent():
    session.clear()
    return render_template("login.html",msg="You have been logged out!!!")

@app.route('/logoutlecturer')
@login_requiredlecturer
def logoutlecturer():
    session.clear()
    return render_template("login.html",msg="You have been logged out!!!")

@app.route('/webcamrec')
def webcamrec():
    return Response(getframe(),mimetype='multipart/x-mixed-replace; boundary=frame')

#face recognition code for attendance
def getframe():
    camera_port=cv2.CAP_DSHOW     
    ramp_frames=100
    i=1
    facecascade=cv2.CascadeClassifier('Classifier/haarcascade_frontalface_default.xml')
    recognizer=cv2.face.EigenFaceRecognizer_create()
    recognizer.read("Training Data/trainingDataEigen.yml")
    camera=cv2.VideoCapture(camera_port)#this makes a web cam object
    camera.set(5,60)
    def FileRead():
        Info = open("Rollno's.txt", "r")
        global Rollno
        Rollno = {}
        while (True):                                   
            Line = Info.readline()
            if Line == '':
                break
            split= Line.split(",")
            key=split[0]
            val=split[1]
            valedit=len(val)-1
            val=val[0:valedit]
            Rollno[int(key)] = val
        return Rollno
    FileRead()          
    ID=0
    fontface=cv2.FONT_HERSHEY_DUPLEX
    fontscale=.9
    fontcolor=(255,255,255)
    while True:
        ret,img = camera.read()
        img = cv2.flip(img, 1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=facecascade.detectMultiScale(gray,1.3,5)
        attendance='Present'
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(75,238,255),2)
            ID,conf=recognizer.predict( cv2.resize(gray[y:y+h,x:x+w],(300,300)))
            #print(ID,round(conf))
            if(conf<6500):
                roll=str(Rollno.get(ID))
                if roll not in rollnoatt:
                    rollnoatt.append(roll)
                #cv2.putText(img,Rollno.get(ID),(x+h-145,y-50),fontface,fontscale,fontcolor)
                cv2.putText(img,"Present",(x+h-135,y-20),fontface,fontscale,fontcolor)
                connection=mysql.connect()
                cur=connection.cursor()
                count=1
                for uname in rollnoatt:
                    cur.execute("UPDATE student SET Course='"+course+"',Attendance='"+attendance+"',DateandTime='"+startdatetime+"' where Section='"+section+"' and Username='"+uname+"'")                                                 
                connection.commit()                
                #conf=" {0}%".format(round(100-conf))
            else:
                ID="Not Registered"
                cv2.putText(img,str(ID),(x+h-175,y-20),fontface,fontscale,fontcolor)
                #conf=" {0}%".format(round(100-conf))      
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
    camera.release()
    del(camera)
    cv2.destroyAllWindows()

#attendance mgmt. code       
@app.route('/webcamstop')
def webcamstop():
    connection=mysql.connect()
    cur=connection.cursor()
    attendance="Absent"
    attendancep="Present"
    date=datetime.now()
    enddatetime=date.strftime('%Y-%m-%d %I:%M %p')
    uname=tuple(rollnoatt)
    unamecount=len(uname)
    #absentees attendance in student database temporary for sending mail
    if(unamecount==0):
        cur.execute("UPDATE student SET Course='"+course+"',Attendance='"+attendance+"',DateandTime='"+startdatetime+"' where Section='"+section+"'")
    elif(unamecount==1):
        cur.execute("UPDATE student SET Course='"+course+"',Attendance='"+attendance+"',DateandTime='"+startdatetime+"' where Section='"+section+"' and Username NOT IN (%s)",rollnoatt)
    else:
        cur.execute("UPDATE student SET Course='"+course+"',Attendance='"+attendance+"',DateandTime='"+startdatetime+"' where Section='"+section+"' and Username NOT IN "+str(tuple(rollnoatt)))
    connection.commit()
    #store present member details in attendance database
    cur.execute("SELECT Username from student where Section='"+section+"' and Attendance='"+attendancep+"'")
    dataroll=cur.fetchall()
    for row in dataroll:
        rollnumb=str(row[0])
        endpt=datetime.strptime(enddatetime,'%Y-%m-%d %I:%M %p')
        endperiodtime=str(endpt.strftime('%I:%M %p'))
        cur.execute("INSERT INTO attendance (Username,Section,Course,Attendance,StartPeriodTime,EndPeriodTime) VALUES(%s,%s,%s,%s,%s,%s)",(rollnumb,section,course,attendancep,startdatetime,endperiodtime))
    connection.commit()
    #store absent member details in attendance database
    cur.execute("SELECT Username from student where Section='"+section+"' and Attendance='"+attendance+"'")
    datauname=cur.fetchall()
    for row in datauname:
        rollnum=str(row[0])
        endpt=datetime.strptime(enddatetime,'%Y-%m-%d %I:%M %p')
        endperiodtime=str(endpt.strftime('%I:%M %p'))
        cur.execute("INSERT INTO attendance (Username,Section,Course,Attendance,StartPeriodTime,EndPeriodTime) VALUES(%s,%s,%s,%s,%s,%s)",(rollnum,section,course,attendance,startdatetime,endperiodtime))
    connection.commit()
    #code to update att percentage
    cur.execute("SELECT Username from student where Section='"+section+"'")
    rollnumber=cur.fetchall()
    for row in rollnumber:
        rollnumber=str(row[0])
        cur.execute("SELECT count(Course) from attendance where Section='"+section+"' and Username='"+rollnumber+"'")
        totalclasses=cur.fetchone()
        totalclasses=int(totalclasses[0])
        cur.execute("SELECT count(Attendance) from attendance where Section='"+section+"' and Username='"+rollnumber+"' and Attendance='Present'")
        presentclasses=cur.fetchone()
        presentclasses=int(presentclasses[0])
        if (presentclasses==totalclasses==0):
            Percentage="0.0"
        else:
            Percentage=float((presentclasses/totalclasses)*100)
            Percentage=str("{0:.1f}%".format(Percentage))
        cur.execute("UPDATE student SET AttPercentage='"+Percentage+"' where Section='"+section+"' and Username='"+rollnumber+"'")
        connection.commit()
    #info to send email
    cur.execute("SELECT Fullname,ParentsEmailid,Course,DateandTime FROM student WHERE Section='"+section+"' and Attendance='"+attendance+"'")
    data=cur.fetchall()
    for row in data:
        startp=datetime.strptime(startdatetime,'%Y-%m-%d %I:%M %p')
        endp=datetime.strptime(enddatetime,'%Y-%m-%d %I:%M %p')
        startperiod=str(startp.strftime('%Y-%m-%d (%I:%M %p'))
        endperiod=str(endp.strftime('- %I:%M %p)'))
        msg = Message('KITSW '+row[0]+' Attendance Report',recipients= [row[1]])
        msg.body = "Dear Parent your ward "+row[0]+" was absent to the following classes held on "+row[2]+" "+startperiod+" "+endperiod+"-KITSW"
        msg.html = "<p><b>Dear Parent,</b></p><p align='justify'>Your ward <strong>"+row[0]+"</strong> was absent to the following classes <strong>"+row[2]+"</strong> held on <strong><span style='color:blue;'>"+startperiod+" "+endperiod+"</span>.</strong></p><p><b>KITSW</b></p>"
        mail.send(msg)
    return render_template("adminhome.html")

if __name__=="__main__":
    #app.config['SERVER_NAME'] = "localhost:4000"
    app.run(host='0.0.0.0',port='4000',debug='True')
    
