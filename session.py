import time
import os
from urllib.parse import parse_qsl

def authed():
	session = dict(parse_qsl(os.environ.get("HTTP_SESSION")))
	try:
		assert( int(session["untill"]) >= int(time.time()) )
	except:
		return False

	return True

def authredirect(url=os.environ.get("REQUEST_URI")):
	print("Status: 401 Not authorized\r")
	print(f"X-Session: &redirect={url}\r")
	print("Refresh: 3;url=/auth\r")
	print("Content-Type: text/plain\r\n\r")
	print("Not logged in; Redirecting...")
	exit()

