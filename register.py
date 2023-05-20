from datetime import datetime
from flask import Flask, render_template,request,json,redirect 
import mysql.connector                          
from collections.abc import Mapping
from sqlalchemy import true 
from flask   import session
import face_recognition
import cv2 
import bcrypt
import bson.binary 
import base64
from io import BytesIO
import numpy as np
import pandas as pd
from base64 import b64encode
from datetime import datetime
import os
from PIL import Image 
from flask_mail import Mail 
import csv
import xlsxwriter
import openpyxl

app = Flask(__name__)
app.secret_key = 'hello how are you'

app.config['adminimages'] = 'C:/Users/A shaikh/Desktop/flask/check_in/adminimages'
app.config['cropped'] = 'C:/Users/A shaikh/Desktop/flask/check_in/croppedimages'

#db connection
conn= mysql.connector.connect(host="localhost",user="root",port="3307",password="",database="checkin")

#Sending Email
with open('config.json','r') as c:
    params = json.load(c)["params"]
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail'],
    MAIL_PASSWORD = params['password']
)   # for mail
mail = Mail(app)    


@app.route("/")
def main():
    return render_template('index.html')
  

@app.route('/signup')
def Showsignup():
    return render_template('signup.html')

@app.route('/api/signup',methods=['POST'])
def signUp():
    try:
        username = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        pic=request.files['photo'] 
        # read the image data
        img_data = pic.read()
        # create a binary object from the image data
        img_binary = bytes(img_data)
            # create a numpy array from the image data
        nparr = np.frombuffer(img_data, np.uint8)
        # decode numpy array as image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
        # detect faces in the image
        face_locations = face_recognition.face_locations(img)
        # detect faces in the image
        face_locations = []
        if len(img) > 0:
            face_locations = face_recognition.face_locations(img)
        # check if exactly one face was detected
        if len(face_locations) == 1:                                
                # get the face encoding
                face_encoding = face_recognition.face_encodings(img, face_locations)[0]

                 # create a binary object from the face encoding
                face_encoding_binary = bytes(face_encoding.tobytes()) 

                print(pic)
                if not pic:
                    return 'No pic uploaded!', 400
                filename = pic.filename
                mimetype = pic.mimetype
                if not filename or not mimetype:
                    return 'Bad upload!', 400
                print("pic",pic)

                selectquery = "select * from accounts where username ='%s' "%username
                cursor=conn.cursor()
                cursor.execute(selectquery)
                data = cursor.fetchall()
                if len(data)== 0:
                    conn.commit()
                    insertquery = "INSERT INTO accounts (id, username, password, email,filename, img_binary, face_encoding_binary) VALUES (null, %s, %s, %s, %s, %s, %s)"
                    values = (username, password, email, filename, img_binary,face_encoding_binary)
                    cursor.execute(insertquery, values)
                    conn.commit()
                    cursor.close() 
                    return render_template('signup.html')
            
                else:
                    return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error':str(e)})  

        
@app.route('/signin')
def showSignin():
    return render_template('signin.html')


@app.route('/api/validateLogin',methods=['POST'])
def validateLogin():
    try:
        email = request.form['inputEmail']
        password = request.form['inputPassword']
 
     # connect to mysql
        print("before proce")
        cursor=conn.cursor()
        cursor.execute("select * from accounts where email ='%s' and password='%s'"%(email,password))
        print('after proc')
        data = cursor.fetchall()
        conn.commit()
        print(data)
        if len(data) > 0:
            session['userid'] = data[0][0]
            print('inside if')
            return  render_template('userhome.html',accounts=data)
            
        else:
            return render_template('error.html',error = 'Wrong Email address or Password')
 
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/blog') 
def blog():
    return render_template('blog.html')

@app.route('/userHome')     
def userHome():
    if session.get('userid'):
        cursor = conn.cursor(buffered=true)
        username =str(session.get('userid'))
        selectquery="select username from accounts where username='%s'"%(username)
        print(selectquery)  
        cursor.execute(selectquery) 
        data= cursor.fetchall() 
        print(data)     
        cursor.close()  
        return render_template('userhome.html',username=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')



@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/profile')
def profile():  
    if session.get('userid'):   
        cursor = conn.cursor(buffered=true)
        userid =int(session.get('userid'))
        selectquery="Select * from accounts where id=%d"%(userid)
        print(selectquery)
        cursor.execute(selectquery)
        data= cursor.fetchall()
        print(data)       
        cursor.close()
        return render_template('userprofile.html',userprofile=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/Showappointment')       
def Showregister():
    return render_template('appointment.html')


@app.route("/appointment",methods=['GET','POST'])
def registerr():
    if session.get('userid'):
        
        if request.method=='POST': 
            reg=request.form
            fname=str(reg['fname'])
            lname=str(reg['lname'])
            contact=int(reg['contact'])
            aadhar=int(reg['aadhar'])
            gender=str(reg['gender'])
            docn=str(reg['docn'])
            time=str(reg['time'])
            cond=str(reg['condition']) 
            dat=str(reg['dat']) 
            eemail=str(reg['eemail'])
                
            user = int(session.get('userid'))
            cursor=conn.cursor()
            query="insert into register values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (fname,lname,contact,aadhar,gender,docn,time,cond,user,dat,eemail) 
            cursor.execute(query, values)
            conn.commit()
            cursor.close()

            message = f'Your Appointment has been confirmed \n on {dat} at {time} \n with {docn} of Our Hospital'
            mail.send_message('New Message from City Hospital for' + fname,sender=params['gmail'],recipients = [eemail],body="message : "+message)
            return render_template('appointment.html')  

        else:
            return render_template('appointment.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')



@app.route('/Viewappointment')
def viewAppointment():
    if session.get('userid'):
        print("if ke andar")
        # pid = (session.get('pid'))
        userid = int(session.get('userid'))
        cursor = conn.cursor(buffered=true)
        selectquery=("select * from register where user_id=%d ORDER by pid DESC")%(userid)
        print(userid)
        cursor.execute(selectquery)
        data= cursor.fetchall()
        print(data) 
        cursor.close()
        return render_template('viewappointment.html',register=data)
    


@app.route('/delete',methods=['POST'])
def delete():
    if session.get('userid'):
        userid = int(session.get('userid'))
        cursor = conn.cursor(buffered=True)
        deletequery = ("DELETE FROM register WHERE user_id=%d ORDER BY pid DESC LIMIT 1" % (userid))
        cursor.execute(deletequery)
        conn.commit()
        cursor.close()
        return json.dumps({'status': 'Appointment Deleted'})  
    else:
        return render_template('error.html', error='Unauthorized Access') 

#retrieves the data from the database
@app.route('/export-data')
def export_data():
    cursor = conn.cursor(buffered=true)
    cursor.execute('SELECT * FROM register')
    data = cursor.fetchall()
    cursor.close()
    return data

#Convert the retrieved data into a CSV file:
@app.route('/export-csv')
def export_csv():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM register')
    data = cursor.fetchall()
    cursor.close()
    
    # convert the data to CSV format
    with open('C:/Users/A shaikh/Desktop/flask/check_in/data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the column headings
        writer.writerow(['Token No.', 'First_name','Last_name','contact','aadhar','gender',	'doc_Type',	'time',	'condition','user_id','date','Email'])
        # Write the data rows
        for row in data:
            writer.writerow(row)
        
    
    return 'Data exported to CSV file in to the path allocated.'






# ADMIN PAGE

@app.route('/admin')
def showadmin():
    cursor = conn.cursor(buffered=true)
    selectquery=("SELECT * FROM register ORDER BY pid DESC")  
    cursor.execute(selectquery)
    data= cursor.fetchall()
    print(data) 
    cursor.close()
    return render_template('admin.html',register=data)

@app.route('/report')
def report():
    return render_template('report.html')


@app.route("/compare_face", methods=['GET', 'POST'])
def compare_face():
    if request.method == 'POST':
        # read the image data sent by the admin
        pic = request.files['photo']
        img_data = pic.read() 
        # create a numpy array from the image data
        nparr = np.frombuffer(img_data, np.uint8)
        # decode numpy array as image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # detect faces in the image
        face_locations = face_recognition.face_locations(img)
        if len(face_locations) == 1:
            # get the face encoding
            face_encoding = face_recognition.face_encodings(img, face_locations)[0]
            # get the user_id and all the face_encodings from the database
            cursor = conn.cursor()
            query = "SELECT id, face_encoding_binary FROM accounts"
            print(query)                                    
            cursor.execute(query)
            rows = cursor.fetchall()
            # loop over all the face_encodings and compare with the current face_encoding
            matching_user_id = []
            for row in rows:
                if row[1] is not None:
                    stored_encoding = np.frombuffer(row[1], dtype=np.float64)
                    stored_encoding = stored_encoding.reshape(1, -1)
                    distance = face_recognition.face_distance(stored_encoding, face_encoding)
                    if distance < 0.6:  # set a threshold for distance
                        # found a match, get the user_id
                        matching_user_id.append(row[0])
                        # matching_user_id.append(matching_user_id)
                        break
            if matching_user_id :
                # match found, get the appointments registered by the user
                for user_id in matching_user_id:
                    query = "SELECT * FROM register WHERE user_id = %s and  date=CURRENT_DATE();"
                    cursor.execute(query, (user_id,))
                    rows = cursor.fetchall()


                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")                
                    filename = f"appointments"+timestamp+".xlsx"
                    excel_file = os.path.join(app.root_path, filename)

                    # create a pandas dataframe with the matching appointments
                    df = pd.DataFrame(rows, columns=["Token", "first_name", "last_name", "contact", "aadhar", "gender", "doc_type", "time", "condition", "user_id", "date", "Email"])
                    # append timestamp to the dataframe
                    df['timestamp'] = timestamp
                    # append the DataFrame to the existing Excel file or create a new file
                    try:
                        # check if the Excel file exists
                        book = openpyxl.load_workbook(excel_file)
                        writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') 
                        writer.book = book
                        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
                        df.to_excel(writer, sheet_name='Appointments', index=False, header=False, startrow=writer.sheets['Appointments'].max_row)
                        writer.close()
                    except FileNotFoundError:
                        # save the DataFrame as a new Excel file
                        writer = pd.ExcelWriter(excel_file, engine='openpyxl') 
                        df.to_excel(writer, sheet_name='Appointments', index=False)
                        writer.close()


                # render the template with the matching appointments
                return render_template('match.html', rows=rows)

            else:
                # no match found                    
                return render_template('no_face.html')
        else:
            # no or multiple faces detected in the image
            return render_template('error.html', error='Please upload an image with exactly one face')
    else:
        # display the form to upload the image
        return render_template('admin.html')



if __name__ =='__main__':
    app.run(debug=True)    