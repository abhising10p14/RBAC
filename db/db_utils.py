from db import db_conn
from log.logger import getLogger
from data import tables_data

logger = getLogger()


def create_table():
    for table_name in tables_data.TABLES:
        table_description = tables_data.TABLES[table_name]
        logger.debug("Creating table {}: ".format(table_name))
        result,code = db_conn.execute_query(table_description)
        if result is None and code != 200:
			logger.error("Failed creating database " + str(code))



