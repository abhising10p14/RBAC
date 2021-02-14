from datetime import datetime

def getuUid():
	currentTime = str(datetime.now())
	uUid  = currentTime.replace(" ",'')
	uUid  = uUid.replace(":",'-')
	uUid  = uUid.replace(".",'-')
	return uUid

def getTime():
	currentTime = str(datetime.now())
	currentTime = currentTime.replace(" ",'')
	currentTime  = currentTime.replace(":",'-')
	currentTime  = currentTime.replace(".",'-')
	return currentTime