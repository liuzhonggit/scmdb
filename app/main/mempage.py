from flask import Blueprint,render_template,request
from app import db

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
mem_page=Blueprint('mem_page',__name__,url_prefix='/mem')
@mem_page.route('/')
def mem_index():
	return render_template('mem.html')
@mem_page.route('/meminfo')
def meminfo():
	from app.models import Mem
	mem_res = Mem.query.all()
	ct=request.args.get('create_time')
	new_res = {'x':[],'data':[]}
	for items in mem_res:
		if ct and ct >=items.create_time:
			continue
		new_res['x'].append(items.create_time)
		new_res['data'].append(items.mem)
	if len(new_res['x'])>=1:
		new_res['max_time'] = new_res['x'][-1]
	else:
		new_res['max_time'] =ct
	return json.dumps(new_res)