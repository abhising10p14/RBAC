import logging
from logging.handlers import RotatingFileHandler
from util import utils

LOGLEVEL = logging.DEBUG #TODO: this should be taken from config 
LOGOBJ = None

def getLogger():
	global LOGOBJ
	if LOGOBJ is None:
		LOGOBJ = logging.getLogger(__name__)
		logFileName =  "logFile.log"
		handler = RotatingFileHandler(logFileName, maxBytes=20000, backupCount=10)
		LOGOBJ.addHandler(handler)
		LOGOBJ.setLevel(LOGLEVEL)
	return LOGOBJ