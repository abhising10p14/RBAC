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
	global DBSESSION
	logger.debug("authenticate one employee")
	query = db_scripts.SCRIPTS['get_from_auth_table']
	# logger.debug("look for " + username + " : " + password)
	if DBSESSION:
		try:
			DBSESSION.cursor.execute(query,  (str(username), str(password)) )
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logger.error('error executing query "{}", error:   {}'.format(query , error))
			code = 500
		else:
			
			code = 200
			if len(result) == 0:
				code = 403
			return result,code
	else:
		logger.error("DB session not up")
		return None, 500


def execute_multiple_queries( DBSESSION,statements_and_values, rollback_on_error=True):
	"""
	Execute multiple SQL statements and returns the cursor from the last executed statement.
	rollback_on_error: Flag to indicate action to be taken on an exception
	:type rollback_on_error: bool

	:param statements_and_values: The statements and values to be executed
    :type statements_and_values: A list of lists. Each sublist consists of a string, 
    	the SQL prepared statement with %s placeholders, and a list or tuple of its 
    	parameters


	:returns cursor from the last statement executed
	:rtype cursor
	"""

	query_index  = 0
	values_index = 1
	try:
		for s_v in statements_and_values:
			DBSESSION.cursor.execute(s_v[query_index], s_v[values_index])
			if not rollback_on_error:
				DBSESSION.connection.commit() # commit on each statement
	except Exception as e:
		if rollback_on_error:
			DBSESSION.connection.rollback()
			return DBSESSION.cursor, 500
	else:
		if rollback_on_error:
			DBSESSION.connection.commit() # then commit only after all statements have completed sucessfuly
		return DBSESSION.cursor #


def insert_into_employees_table(dict):
	global DBSESSION
	logger.debug("INSERT INTO EMPLOYEES TABLES ")
	# first insert into role table :
	role_query = db_scripts.SCRIPTS['insert_into_role_table'];
	employee_query = db_scripts.SCRIPTS['insert_into_employees_table'];
	qyery_list = [ [role_query, dict['role_data']], [employee_query, dict['employee_data']] ]
	if DBSESSION:
		cursor, code = execute_multiple_queries(DBSESSION,qyery_list,True)
		if code == 500:
			return None, code
		if code == 201:
			logger.debug("Inserted into employees and role")
			return cursor.fetchall(), code
	else:
		logger.error("db session not up")
		return None, 500


def get_data_from_role_table(role_id):
	global DBSESSION
	logger.debug("get role from role table")
	query = db_scripts.SCRIPTS['get_from_role_table']
	if DBSESSION:
		try:
			DBSESSION.cursor.execute(query,  (role_id,) )
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logger.error('error executing query "{}", error:   {}'.format(query , error))
			code = 500
		else:
			
			code = 200
			if len(result) == 0:
				code = 404
			return result,code
	else:
		logger.error("DB session not up")
		return None, 500

def get_data_from_employees_table(emp_mail):
	global DBSESSION
	logger.debug("get employee from employee table")
	query = db_scripts.SCRIPTS['get_from_employee_table']
	if DBSESSION:
		try:
			DBSESSION.cursor.execute(query,  (emp_mail,) )
			result = DBSESSION.cursor.fetchall()
		except Exception as error:
			logger.error('error executing query "{}", error:   {}'.format(query , error))
			code = 500
		else:
			
			code = 200
			if len(result) == 0:
				code = 404
			return result,code
	else:
		logger.error("DB session not up")
		return None, 500

