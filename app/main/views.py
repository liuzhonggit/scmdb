#! /bin/env python
# conding:utf-8
from flask import request,redirect,render_template,session
# from flask_sqlalchemy import SQLAlchemy
import logpage
import mempage
from dbutils import db
import json
from functools import wraps
import tokenutil
import requests
import sys
from app import app,db
from app.models import User,Idc,Pc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# app=Flask(__name__)
app.register_blueprint(logpage.log_page)
app.register_blueprint(mempage.mem_page)
app.secret_key="dsfdsf%$&^*1243GHkjkkkjhGFF5545657*(*@@*&&^%$$%asfddsf1242432544351HJHH55GGhhjjj$^%^43fds"
def login_required(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		if not session.get('user'):
			return redirect('/login')
		# token=request.args.get('token')
		# if not token:
		# 	return json.dumps({'code':1})
		# token_res=tokenutil.verify_token(token)
		# if token_res['code'] ==0:
		# 	return f(*args,**kwargs)
		return f(*args,**kwargs)
		# return json.dumps(token_res)
	return decorated_function

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method =='GET':
		 return render_template('login.html')
	if request.method == 'POST':
		user = request.form.get('user')
		pwd = request.form.get('pwd')
		# res = db.list('user','*',{'user':user,'password':pwd})
		res =User.query.filter_by(user=user,password=pwd).first()
		print res
		if res:
			# return json.dumps({'code':0,'access_token':tokenutil.create_token(res[0][1],res[0][3])})
			session['user']=user
			return redirect('/pc')
			app.logger.info('login success')
		else:
			return json.dumps({'code':1})
			# return 'falied'
			app.logger.error('login failed. Please check your user or password!')
@app.route('/logout',methods=['GET','POST'])
def logout():
	del session['user']
	return redirect('/login')
@app.route('/')
def index():
	return redirect('/pc')
@app.route('/user')
@login_required
def user():
	return render_template('user.html')
@app.route('/idc')
@login_required
def idc():
	return render_template('idc.html')
@app.route('/pc')
@login_required
def pc():
	return render_template('pc.html')
@app.route('/count')
def count():
	return render_template('count.html')
@app.route('/log')
def log():
	return render_template('log.html')
@app.route('/pcount')
def pcount():
	# res=db.list('pc')
	res=Pc.query.all()
	pc_count={'names':[],'data':[]}
	mem_dict={}
	for items in res:
		mem_dict[items.mem]=mem_dict.get(items.mem,0)+1
	for m,count in mem_dict.items():
		mem = str(m)+'G'
		pc_count['names'].append(mem)
		pc_count['data'].append({'value':count,'name':mem})
	return json.dumps(pc_count)
@app.route('/loginfo')
def loginfo():
	with open('log.log') as f:
		res={}
		for log in f:
			if log == '\n' or log==' ':
				continue
			l = log.split()
			# print l
			ip,status=l[0],l[8]
			res[(ip,status)]=res.get((ip,status),0)+1
		print res.keys()
		map_url='http://api.map.baidu.com/location/ip'
		ak='EZjjhRLSUcbrf6E8RBwBHYdn1dywMntD'
		for (ip,status),count in res.items():
			url='%s?&ak=%s&ip=%s&coor=bd09ll'%(map_url,ak,ip)
			a=requests.get(url)
			print a.json()
			if a.json()['status'] == 0:
				x=a.json()['content']['point']['x']
				y=a.json()['content']['point']['y']
				# add_log=db.insert('log',{'ip':ip,'status':status,'x':x,'y':y,'count':count})
				add_log=log(ip,status,x,y,count)
				db.session.add(log)
				print 'add success'
		db.session.commit()
	return 'ok'       
@app.route('/addapi',methods=['POST'])
def addapi():
	res_dict = request.form.to_dict()
	print res_dict
	table_name = res_dict.pop('table_name')
	if table_name =='pc':
		ip,cpu,mem,disk,idc,buy_date,comments=res_dict['ip'],res_dict['cpu'],res_dict['mem'],res_dict['disk'],res_dict['idc'],res_dict['buy_date'],res_dict['comments']
		add_pc=Pc(ip,cpu,mem,disk,idc,buy_date,comments)
		db.session.add(add_pc)
	if table_name == 'idc':
		name,area=res_dict['name'],res_dict['area']
		add_idc=Idc(name,area)
		db.session.add(add_idc)
	print db.session.commit()
	return json.dumps({'code':0})
	# add_idc = db.insert(table_name,idc_dict)
	# return json.dumps(add_idc)
@app.route('/listapi')
@login_required
def listapi():
	# access_token=request.args.get('token')
	# print access_token
	# if not access_token:
	# 	return json.dumps({'code':1,'msg':'null token'})
	# token_res=tokenutil.verify_token(access_token)
	# if token_res['code']>0:
	# 	return json.dumps(token_res)
	table_name=request.args.get('table_name')
	# list_res=db.list(table_name)
	list_res=[]
	if table_name=='pc':
		res=Pc.query.all()
		for items in res:
			list_res.append([items.id,items.ip,items.cpu,items.mem,items.disk,items.idc,items.buy_date,items.comments])
	elif table_name=='idc':
		res=Idc.query.all()
		for items in res:
			list_res.append([items.id,items.name,items.area])
	print list_res
	new_res=[]
	for i in range(len(list_res)):
		new_res.append(list_res[i]+[i+1])
	print json.dumps(new_res)
	return json.dumps(new_res)
@app.route('/delete',methods=['POST'])
def delete():
	table_name=request.form.get('table_name')
	value=request.form.get('value')
	# print value,table_name
	if table_name =='pc':
		res=Pc.query.filter_by(id=value).first()
	elif table_name=='idc':
		res=Idc.query.filter_by(id=value).first()
	print str(Pc.query.filter_by(id=value))
	print res
	# print res,table_name,value
	db.session.delete(res)
	db.session.commit()
	print res,table_name,value
	# delete_res=db.delete(table_name,col_name,value)
	# print delete_res
	return 'ok'
@app.route('/update',methods=['POST'])
def update():
	res_dict=request.form.to_dict()
	print res_dict
	table_name=res_dict.pop('table_name')
	row_id=res_dict.pop('id')
	print res_dict
	if table_name =='pc':
		res=Pc.query.filter_by(id=row_id).first()
		res.ip,res.cpu,res.mem,res.disk,res.idc,res.buy_date,res.comments=res_dict['ip'],res_dict['cpu'],res_dict['mem'],res_dict['disk'],res_dict['idc'],res_dict['buy_date'],res_dict['comments']
		db.session.add(res)
	elif table_name=='idc':
		res=Idc.query.filter_by(id=row_id).first()
		res.name,res.area=res_dict['name'],res_dict['area']
		db.session.add(res)
	db.session.commit()
	return 'ok'
	# update_res=db.update(table_name,row_id,args)
	# return update_res
# if __name__=='__main__':
# 	app.run(host='0.0.0.0',port=80,debug=True)
