from flask import Blueprint,render_template
from flask import Flask, redirect ,url_for,render_template,request,session,flash
from .models import User,Doctor
from .models import Appointment
from werkzeug.security import generate_password_hash,check_password_hash

from .__init__ import db
from flask import *  
from flask_mail import Mail  ,Message
from random import *  
 
import os
from email.message import EmailMessage
import ssl
import smtplib

from datetime import date

from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth', __name__)


@auth.route('/home')
def home():
    email=session['email']
    Summa=Appointment.query.filter(Appointment.Doctormail==email).all()
    
    return render_template("home.html",user=current_user,summa=Summa)

@auth.route('/login',methods =['GET','POST'])
def login():
    
    if request.method =='POST':
     email=request.form.get('email')
     password=request.form.get('password')
     session['email']=email
     user=User.query.filter_by(email=email).first()
     doctor=Doctor.query.filter_by(email=email).first()
     if user:
         if check_password_hash(user.password,password):
             flash('Patient Logged in successfully!',category='success')
             session['user']='patient'
             login_user(user,remember=True)
             return redirect(url_for('auth.home_patient'))
         
         else:
             flash('Incorrect password ,try again.',category='error')
     elif doctor:
         if check_password_hash(doctor.password,password):
             flash('Doctor Logged in successfully!',category='success')
             session['user']='doctor'
             login_user(doctor,remember=True)
             return redirect(url_for('auth.home'))
         
         else:
             flash('Incorrect password ,try again.',category='error')
     else:
         flash('Email does not exist',category='error')
     
    return render_template("login.html",user=current_user)





@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/verify',methods = ["GET","POST"])  
def verify():
    
    if request.method=='POST':
        return redirect(url_for('auth.validate'))
        

    return render_template("verify.html")
    
    

@auth.route('/validate',methods=["GET","POST"])   
def validate():  
    otp=session['otp']
    
    user_otp = request.form.get('otp') 
    if otp == int(user_otp) and session['user']=='patient':  
        
        password1=session['password']
        email=session['email']
        firstName=session['firstName']
        secondName=session['secondName']
        bloodgroup=session['bloodgroup']
        gender=session['gender']
        phoneNo=session['phoneNo']
        Address=session['Address']
        Emergencycontact=session['Emergencycontact']
        Emergencycontactnum=session['Emergencycontactnum']
        city=session['city']
        
        
        
        new_user=User(email=email,first_name=firstName,second_name=secondName,password=generate_password_hash(password1,method='sha256'),bloodgroup=bloodgroup,phoneNo=phoneNo,city=city,Emergencycontact=Emergencycontact,Emergencycontactnum=Emergencycontactnum,gender=gender,Address=Address)
        db.session.add(new_user)
        db.session.commit()
        session.pop('otp')
        flash('Patient Account created!', category='success')
        return redirect(url_for('auth.home_patient'))
    
    if otp == int(user_otp) and session['user']=='doctor':  
        
        password1=session['password']
        email=session['email']
        firstName=session['firstName']
        secondName=session['secondName']
        gender=session['gender']
        phoneNo=session['phoneNo']
        Address=session['Address']
        city=session['city']
        landmarks=session['landmarks']
        types=session['types']
        fee=session['fee']
        
        new_user=Doctor(email=email,first_name=firstName,second_name=secondName,password=generate_password_hash(password1,method='sha256'),phoneNo=phoneNo,city=city,gender=gender,Address=Address,landmarks=landmarks,types=types,fee=fee)
        db.session.add(new_user)
        db.session.commit()
        session.pop('otp')
        flash('Doctor Account created!', category='success')
        return redirect(url_for('views.home'))
    
        
    flash('OTP does not match', category='error')
    return redirect(url_for('auth.verify'))


@auth.route('/sign_up_patient',methods =['GET','POST'])
def sign_up_patient():
    db.create_all()
    if request.method == 'POST':
        
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        secondName=request.form.get('secondName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        bloodgroup=request.form.get('bloodGroup')
        phoneNo=request.form.get('phoneNo')
        gender=request.form.get('Gender')
        city=request.form.get('city')
        Emergencycontact=request.form.get('Emergencycontact')
        Emergencycontactnum=request.form.get('Emergencycontactnum')
        address=request.form.get('address')
        user=User.query.filter_by(email=email).first()
        

        if user:
            flash('Email already exists',category='error')
        elif len(email) < 8:
            flash('Email must be greater than 7 characters.',category='error')
        elif len(firstName) <4:
            flash('First name should be greater than 4 characters',category='error')
        elif len(secondName)<4:
            flash('Last name should be greater than 4 characters',category='error')
        elif password1 !=password2:
            flash('Passwords are not the same',category='error')
        elif len(password1)<8:
            flash('Passwords should be greater than 7 characters',category='error')
        elif len(phoneNo)!=10 or len(Emergencycontactnum)!=10:
            flash('Enter a valid 10 digit phone number',category='error')
        elif len(city)<=3:
            flash('Enter the proper city',category='error')
        elif len(address)<=10:
             flash('Enter the proper Address',category='error')
        elif len(Emergencycontact)<4:
            flash('the emergency contact name should be greater than 4 characters',category='error')
        elif gender!="Male" and gender!="male" and gender!="female" and gender!="Female" and gender!="others" and gender!="Others":
            flash('The options are male ,female and others',category='error')
            flash('enter a suitable option',category='error')
        else:
            
            sender = "medicalmanagementeam@gmail.com"
            password = "ngwiaxzgetyadyxr" 
            receiver = email
            
            otp = randint(111111,999999)  
            session['user']='patient'
            session['otp']=otp
            session['password']=password1
            session['email']=email
            session['firstName']=firstName
            session['secondName']=secondName
            session['gender']=gender
            session['bloodgroup']=bloodgroup
            session['phoneNo']=phoneNo
            session['city']=city
            session['Emergencycontact']=Emergencycontact
            session['Emergencycontactnum']=Emergencycontactnum
            session['Address']=address
            subject = "OTP"
            body = str(otp)

            en = EmailMessage()
            en["From"] = sender
            en["To"] = receiver
            en["Subject"] = subject
            en.set_content(body)
 
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
             smtp.login(sender,password)
             smtp.sendmail(sender,receiver, en.as_string())
             
            return redirect(url_for("auth.verify"))
            
           
    return render_template("sign_up_patient.html",user=current_user)


@auth.route('/home_patient',methods =['GET','POST'])
@login_required
def home_patient():
    
    if request.method== "POST" :
        search=request.form.get('Search')
        if search!="general" and search!="cardiologist" and search!="gynecologist":
            flash('Doctor type not found',category='error')
            return render_template("home_patients.html",user=current_user)
        else:
          session['seach']=search
          Doct = Doctor.query.all()
          return redirect(url_for("auth.home2_patient",user=current_user,Doctor=Doct,search=search))
            
    return render_template("home_patients.html",user=current_user)


@auth.route('/home2_patient',methods =['GET','POST'])
@login_required
def home2_patient():
    search=session['seach']
    Doct = Doctor.query.all()
    if request.method== "POST" :
        fi=request.form.get('id')
        session['id']=fi
        return redirect(url_for("auth.appointment",user=current_user))
     
    return render_template("home2_patients.html",user=current_user,Doctor=Doct,search=search)      
    

@auth.route('/sign_up_doctor',methods =['GET','POST'])
def sign_up_doctor():
    db.create_all()
    if request.method == 'POST':
        
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        secondName=request.form.get('secondName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        phoneNo=request.form.get('phoneNo')
        gender=request.form.get('Gender')
        city=request.form.get('city')
        address=request.form.get('address')
        landmarks=request.form.get('landmarks')
        types=request.form.get('department')
        fee=request.form.get('fee')
       
        doctor=Doctor.query.filter_by(email=email).first()
            
        if doctor:
            flash('Email already exists',category='error')
        elif len(email) < 8:
            flash('Email must be greater than 7 characters.',category='error')
        elif len(firstName) <4:
            flash('First name should be greater than 4 characters',category='error')
        elif len(secondName)<4:
            flash('Last name should be greater than 4 characters',category='error')
        elif password1 !=password2:
            flash('Passwords are not the same',category='error')
        elif len(password1)<8:
            flash('Passwords should be greater than 7 characters',category='error')
        elif len(phoneNo)!=10 :
            flash('Enter a valid 10 digit phone number',category='error')
        elif len(city)<=3:
            flash('Enter the proper city',category='error')
        elif len(address)<=10:
            flash('Enter the proper Address',category='error')
        elif len(landmarks)<=5:
            flash('Enter the landmarks',category='error')
        elif len(types)<=3:
             flash('Enter the proper type of doctor',category='error')
        elif gender!="Male" and gender!="male" and gender!="female" and gender!="Female" and gender!="others" and gender!="Others":
            flash('The options are male ,female and others',category='error')
            flash('enter a suitable option',category='error')
        else:
            sender = "medicalmanagementeam@gmail.com"
            password = "ngwiaxzgetyadyxr" 
            receiver = email
            session['fee']=fee
            otp = randint(111111,999999)   
            session['user']='doctor'
            session['otp']=otp
            session['password']=password1
            session['email']=email
            session['firstName']=firstName
            session['secondName']=secondName
            session['gender']=gender
            session['phoneNo']=phoneNo
            session['city']=city
            session['Address']=address
            session['landmarks']=landmarks
            session['types']=types
            subject = "OTP"
            body = str(otp)

            en = EmailMessage()
            en["From"] = sender
            en["To"] = receiver
            en["Subject"] = subject
            en.set_content(body)
 
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
             smtp.login(sender,password)
             smtp.sendmail(sender,receiver, en.as_string())
             
            return redirect(url_for("auth.verify"))
            
            
    return render_template("sign_up_doctor.html",user=current_user)


@auth.route('/appointment',methods =['GET','POST'])
@login_required
def appointment():
    fi=session['id']
    Docto = Doctor.query.filter_by(id=fi).first()
    Decto=Doctor.query.filter(Doctor.id==fi).all()
    email=session['email']
    pato=User.query.filter_by(email=email).first()
    patient_email=pato.email
    patient_firstname=pato.first_name
    patient_lastname=pato.second_name
    patientphnno=pato.phoneNo
    doctor_email=Docto.email
    address=Docto.Address
    doctorphnno=Docto.phoneNo
    fee=Docto.fee
    doctor_firstname=Docto.first_name
    doctor_secondname=Docto.second_name
    doctor_Address=Docto.Address
    doctor_fee=Docto.fee
    if request.method == 'POST':
        today=date.today()
        d1 = today.strftime("%Y-%m-%d")
        
        dates=request.form.get('date')
        time=request.form.get('time')
        if dates<d1:
            flash("Enter valid date, you can't book an appointment for an past date",category='error')
            return render_template("appointment.html",user=current_user,fi=fi,Doctor=Decto)
            
        elif  time==0:
            flash('enter valid time',category='error')
            return render_template("appointment.html",user=current_user,fi=fi,Doctor=Decto)
        else:
            sender = "medicalmanagementeam@gmail.com"
            password = "ngwiaxzgetyadyxr" 
            receiver = email
            subject = "Appointment Booking Conformation"
            body = ("Thank You for using our Website, Your appointment has been booked and the doctor has been intimated.\n\n"
                    +"The details of the appointment are as follows\n\n"+"Doctor: "+doctor_firstname+" "
                    +doctor_secondname+"\nClinic Address: "+doctor_Address+"\nTime: "+time+"\nDate: "+dates
                    +"\nDoctor Fee: "+doctor_fee)
            en = EmailMessage()
            en["From"] = sender
            en["To"] = receiver
            en["Subject"] = subject
            en.set_content(body)
            new_user=Appointment(patient_phoneNo=patientphnno,Doctor_phoneNo=doctorphnno,fee=fee,ClinicAddress=address,patientmail=patient_email,date=dates,time=time,patientname=patient_firstname,Doctorname=doctor_firstname,Doctormail=doctor_email)
            db.session.add(new_user)
            db.session.commit()
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
             smtp.login(sender,password)
             smtp.sendmail(sender,receiver, en.as_string())
             
            sender = "medicalmanagementeam@gmail.com"
            password = "ngwiaxzgetyadyxr" 
            receiver = doctor_email
            subject = "Appointment Booked"
            
            body = ("An appointment has been booked using our website.\n\n"
                    +"The details of the appointment are as follows\n\n"+"Patient name: "+patient_firstname+" "
                    +patient_lastname+"\nTime: "+time+"\nDate: "+dates)
            en = EmailMessage()
            en["From"] = sender
            en["To"] = receiver
            en["Subject"] = subject
            en.set_content(body)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
             smtp.login(sender,password)
             smtp.sendmail(sender,receiver, en.as_string())
             
            flash('Details sent via email',category='success')
            return redirect(url_for("auth.confirmed_appointment"))
            
    return render_template("appointment.html",user=current_user,fi=fi,Doctor=Decto)


@auth.route('/confirmed_appointment',methods =['GET','POST'])
@login_required
def confirmed_appointment():
    email=session['email']
    Summa=Appointment.query.filter(Appointment.patientmail==email).all()
    Semma=Appointment.query.filter_by(patientmail=email).all()
    
    
    
    return render_template("confirmed_appointment.html",user=current_user,summa=Summa)      

