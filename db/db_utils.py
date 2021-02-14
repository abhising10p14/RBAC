from db import db_conn
from log.logger import getLogger
from data import tables_data
from db import db_scripts

logger = getLogger()
global DBSESSION
DBSESSION = db_conn.get_db_session()

def create_table():
	global DBSESSION
	result = None
	for table_name in tables_data.TABLES:
		table_description = tables_data.TABLES[table_name]
		logger.debug("Creating table {}: ".format(table_name))
		if DBSESSION:
			try:
				DBSESSION.cursor.execute(table_description)
			except Exception as error:
				logger.error('error execting query "{}", error:   {}'.format(table_description, error))



def get_employeeTable():
	global DBSESSION
	result = None
	code = 500
	logger.debug("getting data of all employee")
	query = db_scripts.SCRIPTS['get_employee_table']
	if DBSESSION:
		try:
			DBSESSION.cursor.execute(query)
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logger.error('error execting query "{}", error:   {}'.format(query, error))
			code = 500
		else:
			code = 200
	return result,code

def get_employee_authentication(username, password):
	logger.debug("authenticate one employee")
	if DBSESSION:
		try:
			DBSESSION.cursor.execute(db_scripts.SCRIPTS['authenticate'],  username, password )
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logger.error('error execting query "{}", error:   {}'.format(query, error))
			code = 500
		else:
			code = 200
			if result is None:
				code = 403
			else:
				return result,code
	else:
		return None, 500

