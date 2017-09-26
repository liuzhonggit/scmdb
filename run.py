from app import app,db,models
import sys
if len(sys.argv) >1:
	if sys.argv[1] == 'create':
		print 'create tables..........'
		db.create_all()
		print 'success................'
if __name__=='__main__':
	import logging
	app.debug=True
	handler=logging.FileHandler('flask.log',encoding='UTF-8')
	handler.setLevel(logging.INFO)
	logging_format=logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0',port=80,debug=True)
