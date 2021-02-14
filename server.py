import sys
sys.path.append("..")


from db import db_utils
from flask import Flask, render_template, request, redirect, url_for
from flask import send_file
from flask import send_from_directory
import os

from util import utils
from log import logger

ISLOGGEDIN = False
ISAUTHREQUIRED = True # ===> pick this from config
logObj = logger.getLogger()
app = Flask(__name__)

@app.route('/server',methods=['GET','POST'])  # writing it for both get and post
def serverMain():
	userIp = request.remote_addr
	uUid = utils.getuUid()
	logObj.debug("accessing /server by :" + userIp + uUid)
	global ISLOGGEDIN
	global ISAUTHREQUIRED
	#first check fro config whether auth is enabled or not 
	#if login is required and 
	#render login page if not logged in
	if ISLOGGEDIN == False and ISAUTHREQUIRED == True:
		return render_template("temp.html")
	else:
		#TODO: call the rbac server next layer 
		log.debug("go to next")
		return render_template("temp.html")

@app.route('/login',methods=['POST'])
def loginServer():
	userIp = request.remote_addr
	uUid = utils.getuUid()
	logObj.debug("accessing /login by :" + userIp + uUid)
	global ISLOGGEDIN
	global ISAUTHREQUIRED
	userName = ""
	passWord = ""
	authSuccess = False
	#if already logged in or if auth is not required we need to proceed to next page 
	if ISLOGGEDIN == False and ISAUTHREQUIRED == True:
		userName = str(request.form.get('username'))
		passWord = str(request.form.get('password'))
		#TODO: call post sql query with given username and password
		#like 
		#authSuccess = sqlQuery()
		authSuccess = True
		if authSuccess == True:
			#TODO: call the rbac server next layer i.e resource page 
			logObj.debug("Successful!")
			return {'username': userName, 'password': passWord}

portNum = 8001  #TODO: get it from config

if __name__ == '__main__':
	db_utils.create_table()
	app.run(host='0.0.0.0', port = portNum, debug=True, threaded=True)
