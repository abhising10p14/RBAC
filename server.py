import sys
sys.path.append("..")



from flask import Flask, render_template, request, redirect, url_for
from flask import send_file
from flask import send_from_directory

import os

from config import config
from db import db_utils
from util import utils
from log import logger


global CONFIGOBJ
global LOGOBJ 

app = Flask(__name__)

@app.route('/server',methods=['GET','POST'])  # writing it for both get and post
def serverMain():
	global CONFIGOBJ
	global LOGOBJ 
	userIp = request.remote_addr
	uUid = utils.getuUid()
	LOGOBJ.debug("accessing /server by :" + userIp + uUid)
	#first check fro config whether auth is enabled or not 
	#if login is required and 
	#render login page if not logged in
	if CONFIGOBJ.auth_enabled:
		return render_template("temp.html")
	else:
		#TODO: call the rbac server next layer 
		LOGOBJ.debug("go to next")
		return render_template("temp.html")

@app.route('/login',methods=['POST'])
def loginServer():
	global CONFIGOBJ
	global LOGOBJ 
	userIp 		= request.remote_addr
	uUid 		= utils.getuUid()
	LOGOBJ.debug("accessing /login by :" + userIp + uUid)
	userName = ""
	passWord = ""
	authSuccess = False
	#if already logged in or if auth is not required we need to proceed to next page 
	if CONFIGOBJ.auth_enabled:
		userName = str(request.form.get('username'))
		passWord = str(request.form.get('password'))
		#TODO: call post sql query with given username and password
		#like 
		#authSuccess = sqlQuery()
		authSuccess = True
		if authSuccess == True:
			#TODO: call the rbac server next layer i.e resource page 
			LOGOBJ.debug("Successful!")
			return {'username': userName, 'password': passWord}



if __name__ == '__main__':
	global CONFIGOBJ
	global LOGOBJ 
	LOGOBJ = logger.getLogger()
	CONFIGOBJ = config.load_config()
	db_utils.create_table()
	app.run(host='0.0.0.0', port = CONFIGOBJ.rbac_port , debug=True, threaded=True)
