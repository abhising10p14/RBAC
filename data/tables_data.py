from config import config
CONFIGOBJ = config.load_config()
TABLES = {}
TABLES['role'] = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "  `role_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `role_name` varchar(50) NOT NULL,"
    "  `user_view` tinyint(1) NOT NULL,"
    "  `user_edit` tinyint(1) NOT NULL,"
    "  `user_delete` tinyint(1) NOT NULL,"
    "  `room_view` tinyint(1) NOT NULL,"
    "  `room_edit` tinyint(1) NOT NULL,"
    "  `room_delete` tinyint(1) NOT NULL,"
    "  PRIMARY KEY (`role_id`)"
    ") ENGINE=InnoDB".format(CONFIGOBJ.role_table_name))

TABLES['employees'] = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "  `emp_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `emp_name` varchar(40) NOT NULL,"
    "  `team` varchar(40) NOT NULL,"
    "  `position` varchar(40) NOT NULL,"
    "  `role` int(11) NOT NULL,"
    "  `phone_number` varchar(20) NOT NULL,"
    "  `email` varchar(100) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`email`),"
    "  FOREIGN KEY (`role`) REFERENCES `role` (`role_id`)"
    ") ENGINE=InnoDB".format(CONFIGOBJ.employees_table_name))

TABLES['room'] = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "  `room_id` int(11) NOT NULL,"
    "  `room_name` varchar(20) NOT NULL,"
    "  `booking_email` varchar(100) NOT NULL,"
    "  `sitting` int(10) NOT NULL,"
    "  `current_status` tinyint(1) NOT NULL,"
    "  PRIMARY KEY (`room_id`),"
    "  FOREIGN KEY (`booking_email`) REFERENCES `employees` (`email`)"
    ") ENGINE=InnoDB".format(CONFIGOBJ.room_table_name))

TABLES['auth'] = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "  `email` varchar(100) NOT NULL UNIQUE,"
    "  `password` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`email`)"
    ") ENGINE=InnoDB".format(CONFIGOBJ.auth_table_name))