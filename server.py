import sys
sys.path.append("..")



from flask import Flask, render_template, request, redirect, url_for
from flask import send_file
from flask import send_from_directory
from collections import defaultdict
import os

from config import config
from db import db_utils
from util import utils
from log import logger


global CONFIGOBJ
global LOGOBJ 
global SESSION
SESSION =  defaultdict(list,{ k:[] for k in ('userIP','username') })

app = Flask(__name__)
@app.route('/server',methods=['GET'])  
def serverMain():
	global SESSION
	global CONFIGOBJ
	global LOGOBJ 
	userIp = request.remote_addr
	uUid = utils.getuUid()
	LOGOBJ.debug("accessing /server by :" + str(userIp) + str(uUid))
	if  userIp in SESSION['userIP'] :
		return 'Logged in as ' + userIp + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
	else:
		if CONFIGOBJ.auth_enabled:
			return render_template(CONFIGOBJ.login_page)
		else:
			LOGOBJ.debug("Auth Not Enabled")
			return render_template(CONFIGOBJ.login_page)

# @app.route('/login',methods=['POST','GET'])
# def loginServer():

@app.route('/login',methods=['GET'])
def loginServer():
	global CONFIGOBJ
	global LOGOBJ 
	global SESSION
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /login by :" + str(userIp) + str(uUid))
	return render_template(CONFIGOBJ.login_page)

@app.route('/authenticate')
def authenticate():
	global CONFIGOBJ
	global LOGOBJ 
	global SESSION
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /login by :" + str(userIp) + str(uUid))
	userName = ""
	passWord = ""
	if CONFIGOBJ.auth_enabled:
		userName = str(request.form.get('username'))
		passWord = str(request.form.get('password'))
		auth_data, authSuccess = db_utils.get_employee_authentication(username,password)
		if authSuccess == 200:
			LOGOBJ.debug("Successful!")
			# adding to session
			# TODO : remove this fromm sessionn after a time if not used 
			SESSION['userIp'].append(userIp)
			SESSION['username'].append(userName)
			employee_data,code = db_utils.get_employeeTable()
			return render_template(CONFIGOBJ.employee_view_page, data=employee_data)
		else:
			return {"Forbidden!!!", 403}
	else:
		employee_data,code = db_utils.get_employeeTable()
		return render_template(CONFIGOBJ.employee_view_page, data=employee_data)


# @app.route('/logout',methods=['GET'])
# def loginServer():


if __name__ == '__main__':
	global CONFIGOBJ
	global LOGOBJ 
	LOGOBJ = logger.getLogger()
	CONFIGOBJ = config.load_config()
	db_utils.create_table()
	app.run(host='0.0.0.0', port = CONFIGOBJ.rbac_port , debug=True, threaded=True)
