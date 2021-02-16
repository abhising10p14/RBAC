import json 



class RBAC_config_base(object):
	def __init__(self):
		self.rbac_port 					= None
		self.auth_enabled 				= False
		self.db_host 					= None
		self.db_username 				= None
		self.db_password 				= None
		self.db_port 					= None
		self.encrpt_key 				= None
		self.server_url 				= None
		self.log_level 					= None
		self.log_output 				= None
		self.database_name 				= None
		self.employees_table_name 		= None
		self.room_table_name			= None
		self.role_table_name			= None
		self.auth_table_name			= None
		self.login_page					= None
		self.employee_view_page			= None
		self.forbidden_page				= None
		self.edit_employee_page			= None
		self.admin_show_table_page  	= None
		self.engg_show_table_page   	= None
		self.default_show_table_page 	= None
		self.office_manager_show_page	= None

CONFIGOBJ 	= None
PROJECTPATH = "/home/abhishek/RBAC/RBAC/config/"
FILENAME 	= "config.json"
def load_config():
	global CONFIGOBJ
	global PROJECTPATH
	global FILENAME
	if CONFIGOBJ is None:
		CONFIGOBJ = RBAC_config_base()
		with open(PROJECTPATH + FILENAME) as f:
			data = json.load(f)
			CONFIGOBJ.rbac_port 				= data['RBAC_PORT']
			CONFIGOBJ.auth_enabled 				= data['AUTHENTICATION_ENABLE']
			CONFIGOBJ.db_host 					= data['DB_HOST']
			CONFIGOBJ.db_username 				= data['DB_USERNAME']
			CONFIGOBJ.db_password 				= data['DB_PASSWORD']
			CONFIGOBJ.db_port 					= data['DB_PORT']
			CONFIGOBJ.encrpt_key 				= data['ENCRYPTION_KEY']
			CONFIGOBJ.server_url 				= data['SERVER_URL']
			CONFIGOBJ.log_level 				= data['LOG_LEVEL']
			CONFIGOBJ.log_output 				= data['LOG_OUTPUT']
			CONFIGOBJ.database_name 			= data['DATABASE_NAME']
			CONFIGOBJ.room_table_name 			= data['ROOM_TABLE']
			CONFIGOBJ.role_table_name 			= data['ROLE_TABLE']
			CONFIGOBJ.employees_table_name 		= data['EMPLOYEE_TABLE']
			CONFIGOBJ.auth_table_name			= data['AUTH_TABLE']
			CONFIGOBJ.login_page				= data['LOGIN_PAGE']
			CONFIGOBJ.employee_view_page		= data['EMPLOYEE_VIEW_PAGE']
			CONFIGOBJ.forbidden_page			= data['FORBIDDEN_PAGE']
			CONFIGOBJ.edit_employee_page		= data['EDIT_EMPLOYEE_FORM']
			CONFIGOBJ.admin_show_table_page		= data['ADMIN_SHOW_TABLE_PAGE']
			CONFIGOBJ.engg_show_table_page		= data['ENGG_SHOW_TABLE_PAGE']
			CONFIGOBJ.default_show_table_page	= data['DEFAULT_SHOW_TABLE_PAGE']
			CONFIGOBJ.office_manager_show_page	= data['OFFICE_MANAGER_SHOW_TABLE']
			
	return CONFIGOBJ




