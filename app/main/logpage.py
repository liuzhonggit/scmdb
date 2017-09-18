from flask import Blueprint,render_template
from app import db
from app.models import Newlog
import requests
import sys
import json
log_page=Blueprint('log_page',__name__,url_prefix='/log')
@log_page.route('/')
def log_index():
    return render_template('log.html')
@log_page.route('/test')
def test():
    return 'xxxxxxxxxxx'
@log_page.route('/data')
def data():
	res=Newlog.query.all()
	log_dict={'data':[],'geo':{}}
	for r in res:
		print r.ip,r.status,r.count
		log_dict['data'].append({'name':r.ip,'value':r.count})
		log_dict['geo'][r.ip]=[r.x,r.y]
	return json.dumps(log_dict)
def press_log():
	with open('log.log') as f:
		res={}
		for log in f:
			if log == '\n' or log==' ':
				continue
			l = log.split()
			# print l
			ip,status=l[0],l[8]
			res[(ip,status)]=res.get((ip,status),0)+1
		# print res.keys()
	map_url='http://api.map.baidu.com/location/ip'
	ak='EZjjhRLSUcbrf6E8RBwBHYdn1dywMntD'
	for (ip,status),count in res.items():
		url='%s?&ak=%s&ip=%s&coor=bd09ll'%(map_url,ak,ip)
		a=requests.get(url)
		print a.json()
		if a.json()['status'] == 0:
			x=a.json()['content']['point']['x']
			y=a.json()['content']['point']['y']
			log=Newlog(ip,status,x,y,count)
			db.session.add(log)
			print 'add success'
	db.session.commit()
	return 'ok'
# if len(sys.argv)>1:
#     if sys.argv[1]=='create':
#         print '*'*50
#         ormdb.create_all()
#         print 'init table'
#     if sys.argv[1]=='log':
#     	press_log()

