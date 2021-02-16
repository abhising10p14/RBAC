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



@app.route('/login',methods=['POST'])
def loginServer():
	global CONFIGOBJ
	global LOGOBJ 
	global SESSION
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /authenticate by :" + str(userIp) + str(uUid))
	userName = ""
	passWord = ""
	if CONFIGOBJ.auth_enabled:
		username = str(request.form.get('username'))
		password = str(request.form.get('password'))
		auth_data, authSuccess = db_utils.get_employee_authentication(username,password)
		if authSuccess == 200:
			LOGOBJ.debug("Successful!")
			# adding to session
			# TODO : remove this fromm sessionn after a time if not used 
			SESSION['userIp'].append(userIp)
			SESSION['username'].append(userName)
			employee_data,code = db_utils.get_employeeTable()
			return render_template(CONFIGOBJ.admin_show_table_page, data=employee_data)
		else:
			LOGOBJ.debug("Invalid ACCESS!!!!" )
			return render_template(CONFIGOBJ.forbidden_page)
	else:
		employee_data,code = db_utils.get_employeeTable()
		return render_template(CONFIGOBJ.employee_view_page, data=employee_data)


# @app.route('/logout',methods=['GET'])
# def loginServer():

def convert_text_to_dictionary(data):
	#preprocess data 
	data = data.split(",")
	data_dict = {}
	data_dict['emp_id']   = data[0].replace('(',"")
	data_dict['emp_name'] = data[1][1:len(data[1]) - 1].replace('u\'',"")
	data_dict['team'] =     data[2][1:len(data[2]) - 1].replace('u\'',"")
	data_dict['position'] =  data[3][1:len(data[3]) - 1].replace('u\'',"")
	data_dict['role_id'] = data[4].replace(' ',"")
	role_name, code = db_utils.get_data_from_role_table(int(data_dict['role_id']))
	if code!= 200:
		return {},code
	else:
		role_name = role_name[0][1]
		data_dict['role_name'] = role_name
	data_dict['phone'] = (data[5][1:len(data[5]) - 1].replace('u\'',"")).replace(' ',"")
	data_dict['email'] = data[6][1:len(data[6]) - 1].replace('u\'',"")
	return data_dict,200


@app.route('/edit_employees')
def edit_empployees():
	global CONFIGOBJ
	global LOGOBJ
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /edit_employees by :" + str(userIp) + str(uUid))
	data = request.args.get('text', default='', type=str)
	data_dict,code = convert_text_to_dictionary(data)
	if code == 200:
		return render_template("edit_EmployeesForm.html", data=data_dict)
	else:
		return code

@app.route('/insertEmployee')
def insert_into_employees():
	global CONFIGOBJ
	global LOGOBJ
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /insertEmployee by :" + str(userIp) + str(uUid))
	name = str(request.form.get('name'))
	team = str(request.form.get('team'))
	position = str(request.form.get('position'))
	phone	= str(request.form.get('phone'))
	role_name = str(request.form.get('phone'))
	



@app.route('/delete_employees')
def delete_empployees():
	global CONFIGOBJ
	global LOGOBJ
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /delete_employees by :" + str(userIp) + str(uUid))

if __name__ == '__main__':
	global CONFIGOBJ
	global LOGOBJ 
	LOGOBJ = logger.getLogger()
	CONFIGOBJ = config.load_config()
	db_utils.create_table()
	app.run(host='0.0.0.0', port = CONFIGOBJ.rbac_port , debug=True, threaded=True)
