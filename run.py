from app import app,db,models
import sys
if len(sys.argv) >1:
	if sys.argv[1] == 'create':
		print 'create tables..........'
		db.create_all()
		print 'success................'
app.run(host='0.0.0.0',port=80,debug=True)