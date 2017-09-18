import time
import psutil as ps
from dbutils import db
def get_mem():
	mem=ps.virtual_memory().available
	create_time=time.time()
	res=db.insert('mem',{'mem':mem,'create_time':create_time})	
	return res
while True:
	get_mem()
	time.sleep(2)