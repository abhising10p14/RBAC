import mysql.connector
from mysql.connector import errorcode
from db import db_const

from log import logger

logObj = logger.getLogger()

class MySQL(object):
	_instance = None
	def __init__(self):
		self.connection = self._instance.connection
		self.cursor = self._instance.cursor
	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)
			# TODO: take this value from db_config.yml
			db_config = {'database': 'rbac', 'host': '127.0.0.1', 
			'password': '10p14aa0071', 'port': 3306, 'user': 'root'}
			try:
				logObj.debug('connecting to MySQL database...')
				connection = MySQL._instance.connection = mysql.connector.connect(**db_config)
				cursor = MySQL._instance.cursor = connection.cursor()
				cursor.execute('SELECT VERSION()')
				db_version = cursor.fetchone()
			except Exception as error:
				logObj.error('Error: connection not established {}'.format(error))
				MySQL._instance = None
			else:
				logObj.info('connection established\n{}'.format(db_version[0]))

		return cls._instance
		
			

DBSESSION = None
def get_db_session():
	global DBSESSION
	if DBSESSION is None:
		DBSESSION = MySQL()
	return DBSESSION


def close_db_session():
	logObj.info("Closing DB session")
	global DBSESSION
	if DBSESSION is None:
		try:
			DBSESSION.connection.close()
		except Exception as e:
			logObj.error("Couldn't close connection: {}".format(e))
		raise e

		try:
			DBSESSION.cursor.close()
		except Exception as e:
			logObj.error("Couldn't close cursor: {}".format(e))
		raise e

def execute_query(query):
	global DBSESSION
	DBSESSION = get_db_session()
	result = None
	code = 500
	logObj.debug("executing query " + query)
	if DBSESSION:
		try:
			result = DBSESSION.cursor.execute(query)
		except Exception as error:
			logObj.error('error execting query "{}", error:   {}'.format(query, error))

		else:
			code = 200
			
	return result,code

