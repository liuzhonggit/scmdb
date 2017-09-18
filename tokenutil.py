import base64
import time
secret_key='dsfgdsg$$%^&^esfreew12321'
def create_token(user,role):
	temp = '%s|%s|%s|%s'%(secret_key,user,role,int(time.time()+60*60*12))
	return base64.b64encode(temp)
print create_token('admin','admin')
def verify_token(token):
	temp=base64.b64decode(token).split('|')
	if len(temp) == 4:
		secret,user,role,expire_time = temp
		if secret == secret_key:
			if int(expire_time) > time.time():
				return {'code':0,'user':user,'role':role}
			else:
				return {'code':1,'msg':'token expires'}
		else:
			return {'code':1,'msg':'wrong key'}
	else:
		return {'code':1,'msg':'wrong token'}

print verify_token('ZHNmZ2RzZyQkJV4mXmVzZnJlZXcxMjMyMXxhZG1pbnxhZG1pbnwxNTAxMzUwMTk0')