#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Sep 26 16:41:03 2022

@author: arundhamodhar
"""

from .__init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):    
    id =db.Column(db.Integer , primary_key=True)
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('doctor.id'))
  
    
class User(db.Model,UserMixin):
    id =db.Column(db.Integer , primary_key=True)
    email =db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    first_name =db.Column(db.String(150)) 
    second_name=db.Column(db.String(150))
    bloodgroup=db.Column(db.String(150))
    gender=db.Column(db.String(150))
    phoneNo=db.Column(db.String(150))
    city=db.Column(db.String(200))
    Emergencycontact=db.Column(db.String(150))
    Emergencycontactnum=db.Column(db.String(150))
    Address=db.Column(db.String(150))
    
    
class Doctor(db.Model,UserMixin):
    id =db.Column(db.Integer , primary_key=True)
    email =db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    first_name =db.Column(db.String(150)) 
    second_name=db.Column(db.String(150))
    gender=db.Column(db.String(150))
    phoneNo=db.Column(db.String(150))
    city=db.Column(db.String(200))
    Address=db.Column(db.String(150))
    landmarks=db.Column(db.String(150))
    types=db.Column(db.String(150))
    fee=db.Column(db.String(150))
    notes=db.relationship('Note')

class Appointment(db.Model,UserMixin):
    id =db.Column(db.Integer,primary_key=True)
    patientname=db.Column(db.String(150))
    Doctorname=db.Column(db.String(150))
    patientmail=db.Column(db.String(150))
    Doctormail =db.Column(db.String(150))
    ClinicAddress=db.Column(db.String(250))
    fee=db.Column(db.String(250))
    patient_phoneNo=db.Column(db.String(150))
    Doctor_phoneNo=db.Column(db.String(150))
    time =db.Column(db.String(150))
    date =db.Column(db.String(150))