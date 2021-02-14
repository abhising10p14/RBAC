import mysql.connector
from mysql.connector import errorcode
from db import db_const
from config import config
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
			# TODO: take this value from config.json
			config_obj = config.load_config()
			db_config = {'database': config_obj.database_name, 'host': config_obj.db_host, 
			'password': config_obj.db_password, 'port': config_obj.db_port, 'user': config_obj.db_username}
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
			DBSESSION.cursor.execute(query)
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logObj.error('error execting query "{}", error:   {}'.format(query, error))

		else:
			code = 200
	return result,code

