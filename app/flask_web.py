# conding:utf-8
from flask import Flask,request,redirect,render_template,session
from flask_sqlalchemy import SQLAlchemy
#from logpage import log_page
from mempage import mem_page
from dbutils import db
import json
from functools import wraps
import tokenutil
import requests
import sys
app=Flask(__name__)
#app.register_blueprint(log_page)
app.register_blueprint(mem_page)
app.secret_key="dsfdsf%$&^*1243GHkjkkkjhGFF5545657*(*@@*&&^%$$%asfddsf1242432544351HJHH55GGhhjjj$^%^43fds"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Pass123!@localhost/python'
db = SQLAlchemy(app)
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
		res = db.list('user','*',{'user':user,'password':pwd})
		print res
		if res:
			# return json.dumps({'code':0,'access_token':tokenutil.create_token(res[0][1],res[0][3])})
			session['user']=user
			return redirect('/pc')
		else:
			# return json.dumps({'code':1})
			return 'login error'
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
@app.route('/mem')
def mem():
	return render_template('mem.html')
@app.route('/count')
def count():
	return render_template('count.html')
@app.route('/log')
def log():
	return render_template('log.html')
@app.route('/meminfo')
def meminfo():
	ct = request.args.get('create_time')
	mem_res = db.list('mem')
	print mem_res
	new_res = {'x':[],'data':[]}
	for items in mem_res:
		if ct and ct >=items[2]:
			continue
		new_res['x'].append(items[2])
		new_res['data'].append(items[1])
	if len(new_res['x'])>=1:
		new_res['max_time'] = new_res['x'][-1]
	else:
		new_res['max_time'] =ct
	return json.dumps(new_res)
@app.route('/pcount')
def pcount():
	res=db.list('pc')
	pc_count={'names':[],'data':[]}
	mem_dict={}
	for items in res:
		mem_dict[items[3]]=mem_dict.get(items[3],0)+1
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
				add_log=db.insert('log',{'ip':ip,'status':status,'x':x,'y':y,'count':count})
	return 'ok'       
@app.route('/addapi',methods=['POST'])
def addapi():
	idc_dict = request.form.to_dict()
	print idc_dict
	table_name = idc_dict.pop('table_name')
	add_idc = db.insert(table_name,idc_dict)
	return json.dumps(add_idc)
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
	list_res=db.list(table_name)
	print list_res
	new_res = []
	for i in range(len(list_res)):
		new_res.append(list(list_res[i])+[i+1])
	print json.dumps(new_res)
	return json.dumps(new_res)
@app.route('/delete',methods=['POST'])
def delete():
	table_name=request.form.get('table_name')
	col_name=request.form.get('col_name')
	value=request.form.get('value')
	print table_name,col_name,value
	delete_res=db.delete(table_name,col_name,value)
	print delete_res
	return delete_res
@app.route('/update',methods=['POST'])
def update():
	args=request.form.to_dict()
	table_name=args.pop('table_name')
	row_id=args.pop('id')
        print args
	update_res=db.update(table_name,row_id,args)
	return update_res
if __name__=='__main__':
	app.run(host='0.0.0.0',port=80,debug=True)
