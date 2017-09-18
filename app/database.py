
# conding:utf-8
from flask_web import db
import requests
import sys
import json

class Newlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(30), unique=False)
    status = db.Column(db.String(20), unique=False)
    x = db.Column(db.String(20), unique=False)
    y = db.Column(db.String(20), unique=False)
    count = db.Column(db.Integer, unique=False)

    def __init__(self,ip,status,x,y,count):
        self.ip = ip
        self.status = status
        self.x = x
        self.y = y
        self.count = count

    def __repr__(self):
        return '<Newlog %r>' % self.ip
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	user = db.Column(db.String(20),unique=False)
	password = db.Column(db.String(30),unique=False)
	type = db.Column(db.String(10),unique=False)

	def __init__(self,user,password,type):
		self.user=user
		self.password=password
		self.type=type
	def __repr__(self):
		return '<User %r>'%self.user
class Idc(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50),unique=False)
	area = db.Column(db.String(50),unique=False)

	def __init__(self,name,area):
		self.name=name
		self.area=area
	def __repr__(self):
		return '<Name %r>'%self.name
class Log(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	ip = db.Column(db.String(20),unique=False)
	status = db.Column(db.String(10),unique=False)
	x = db.Column(db.String(20),unique=False)
	y = db.Column(db.String(20),unique=False)
	count = db.Column(db.Integer,unique=False)

	def __init__(self,ip,status,x,y,count):
		self.ip=ip
		self.status=status
		self.x=x
		self.y=y
		self.count=count
	def __repr__(self):
		return '<Ip %r>'%self.ip
class Mem(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	mem = db.Column(db.String(50),unique=False)
	create_time = db.Column(db.String(50),unique=False)

	def __init__(self,mem,create_time):
		self.mem=mem
		self.create_time=create_time
	def __repr__(self):
		return '<Mem %r>'%self.mem
class Pc(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	ip = db.Column(db.String(50),unique=False)
	cpu = db.Column(db.String(10),unique=False)
	mem = db.Column(db.String(10),unique=False)
	disk = db.Column(db.String(10),unique=False)
	idc = db.Column(db.Integer,unique=False)
	buy_date = db.Column(db.String(20),unique=False)
	comments = db.Column(db.String(200),unique=False)

	def __init__(self,ip,cpu,mem,disk,idc,buy_date,comments):
		self.ip=ip
		self.cpu=cpu
		self.mem=mem
		self.disk=disk
		self.idc=idc
		self.buy_date=buy_date
		self.comments=comments
	def __repr__(self):
		return '<Ip %r>'%self.ip
