# conding:utf-8
import MySQLdb as mysql
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class DB:
	conn=''
	cur=''
	def __init__(self,host,user,password,db):
		self.host=host 
		self.user=user
		self.password=password
		self.db=db
		self.connect()
	def connect(self):
		self.conn=mysql.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,charset="utf8")
		self.conn.autocommit(True)
		self.cur=self.conn.cursor()
	def execute(self,sql):
		try:
			self.cur.execute(sql)
			return self.cur
		except mysql.OperationalError,e:
			print e
			print 'reconnect DB'
			self.connect()
			time.sleep(1)
			return self.execute(sql)
	def list(self,table_name,col_name='*',condition={}):
		sql='select %s from %s'%(col_name,table_name)
		print bool(condition)
		if condition:
			temp = ' and '.join(("%s ='%s'"%item for item in condition.items()))
			sql +=' where ' +temp
			print temp
			print sql
		res=self.execute(sql)
		return res.fetchall()
	def update(self,table_name,row_id,args):
		temp = ("%s='%s'"%item for item in args.items())
		update_value = ','.join(temp)
		sql = 'update %s set %s where id=%s'%(table_name,update_value,row_id)
		print sql
		self.execute(sql)
		return 'ok'
	def delete(self,table_name,col_name,value):
		sql = 'delete from %s where %s = %s'%(table_name,col_name,value)
		self.execute(sql)
		return 'ok'
	def insert(self,table_name,add_dict):
		print add_dict
		if not ''.join(str(add_dict.values())):
			return {'code':1,'msg':'no data'}
		col_names = ','.join(add_dict.keys())
		print col_names
		values = ','.join("'%s'"%v for v in add_dict.values())
		print values
		sql="insert into %s (%s) values (%s)"%(table_name,col_names,values)
		print sql
		self.execute(sql)
		return {'code':0}
db=DB(host='23.106.138.168',user='root',password='Pass123!',db='python')

