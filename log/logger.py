import logging
from logging.handlers import RotatingFileHandler

LOGLEVEL = logging.DEBUG #TODO: this should be taken from config 
LOGOBJ = None

def getLogger():
	global LOGOBJ
	if LOGOBJ is None:
		LOGOBJ = logging.getLogger(__name__)
		handler = RotatingFileHandler('logFile.log', maxBytes=2000, backupCount=10)
		LOGOBJ.addHandler(handler)
		LOGOBJ.setLevel(LOGLEVEL)
	return LOGOBJ