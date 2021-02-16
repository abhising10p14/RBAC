from config import config
CONFIGOBJ = config.load_config()

SCRIPTS = {}
SCRIPTS['get_employee_table'] = ("SELECT * FROM {}".format(CONFIGOBJ.employees_table_name))
SCRIPTS['get_role_table'] 	= ("SELECT * FROM {}".format(CONFIGOBJ.role_table_name))
SCRIPTS['get_room_table'] 	= ("SELECT * FROM {}".format(CONFIGOBJ.room_table_name))

SCRIPTS['insert_into_role_table'] = (
				"INSERT INTO {} ( role_name, user_view,user_edit,"
				"user_delete,room_view, room_edit, room_delete)"
				" Values ( %s , %s , %s ,%s , %s , %s , %s )"
				")".format(CONFIGOBJ.role_table_name))


SCRIPTS['insert_into_employees_table'] = (
				"insert into {} (emp_name ,team, position, role, "
				"phone_number, email) values(%s , %s , %s ,%s , %s"
				" , %s)".format(CONFIGOBJ.employees_table_name))

SCRIPTS['insert_into_room_table'] = (
				"insert into {} (room_id, room_name, booking_email,"
				" sitting, current_status) values (%s , %s , %s ,%s , %s)"
				.format(CONFIGOBJ.room_table_name))


SCRIPTS['insert_into_auth_table'] = (	
			"insert into {} (username, password ) values (%s , %s)"
			")".format(CONFIGOBJ.auth_table_name))

SCRIPTS['delete_from_role_table'] = (
			"delete from {} where role_id = %s".format(CONFIGOBJ.role_table_name))

SCRIPTS['delete_from_employee_table'] = (
			"delete from {} where emp_id = %s".format(CONFIGOBJ.employees_table_name))

SCRIPTS['delete_from_room_table'] = (
			" delete from {} where room_id = %s ".format(CONFIGOBJ.room_table_name))


SCRIPTS['delete_from_auth_table'] = (
			"delete from {} where username = %s AND "
			" password = %s ".format(CONFIGOBJ.auth_table_name))

SCRIPTS['get_from_employee_table'] = (
			"SELECT * FROM {} WHERE email = %s".format(CONFIGOBJ.employees_table_name))

SCRIPTS['get_from_role_table'] = (
			"SELECT * FROM {} WHERE  role_id = %s".format(CONFIGOBJ.role_table_name))


SCRIPTS['get_from_room_table'] = (
			"select * from {} where room_id = %s".format(CONFIGOBJ.room_table_name))


SCRIPTS['get_from_auth_table'] 	= ("SELECT * FROM {} WHERE email  = %s "
						"AND password = %s".format(CONFIGOBJ.auth_table_name))