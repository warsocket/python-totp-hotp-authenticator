#!/usr/bin/env python3
import os
import time
import random
import sys
from urllib.parse import urlparse
from urllib.parse import parse_qsl

#print("Content-Type: text/plain\r\n\r")
#print(os.environ.get("REQUEST_METHOD"))
#sys.stderr = sys.stdout
#exit()

session = dict(parse_qsl(os.environ.get("HTTP_SESSION")))
if not "uuid" in session:
	uuid = "{:08X}-{:04X}-{:04X}-{:04X}-{:012X}".format(random.getrandbits(32), random.getrandbits(16), random.getrandbits(16), random.getrandbits(16), random.getrandbits(48)).lower()
	session['uuid'] = uuid
	print(f"X-Session: uuid={uuid}\r")

#Logout check (when submitted)
if os.environ.get("REQUEST_METHOD") == "DELETE":
        print(f"X-Session: &untill=0&redirect=\r") #logout
        print("Content-Type: text/plain\r\n\r")
        exit()


#OTP check (when submitted)
if os.environ.get("REQUEST_METHOD") == "PUT":
        sys.path.append("/var/www")

        import authenticator
        with open("/var/www/secret", "r") as f: secret = f.read().rstrip()
        if sys.stdin.read() != authenticator.totp(secret):
                print("Status: 401 Unauthorized")
                print("Content-Type: text/plain\r\n\r")
                exit()

        print(f"X-Session: &untill={int(time.time())+3600*24}&redirect=")
        print("Content-Type: text/plain\r\n\r")
        if "redirect" in session: print(session['redirect'], end="")
        exit()


if "untill" in session:
	timeleft = int(session['untill']) - int(time.time())

	d,h = timeleft // 86400, timeleft % 86400
	h,m = h // 3600, h % 3600
	m,s = m // 60, m % 60

	if timeleft >= 0: #Page for logged in user
		print("Content-Type: text/html\r\n\r")
		print(f"""<!DOCTYPE html>
<html>
<head>
<style>
*{{
	box-sizing: border-box;
}}
body{{
	display: flex;
	justify-content: center;
}}
button{{
        font-size: 200%;
        padding: 10px;
	justify-content: center;
}}
div{{
        display: flex;
	flex-direction: column;
}}
font{{
	text-align: center;
	margin:10px;
}}
</style>
</head>
<body>
<div>
<font>Logged in, {timeleft} seconds ({d}d {h:02}:{m:02}:{s:02}) remaining in session</font>
<button id="logoutbutton">Logout</button>
<div>
<script defer>
logoutbutton.addEventListener('click', () => {{
	fetch('', {{method: "DELETE"}}).then(() => document.location.href='')
}})
</script>
</body>
</html>""")
		exit()


#Default page (not logged in)
print("Content-Type: text/html\r")
print("\r")
print("""<!DOCTYPE html>
<html>
<head>
<style>
html,body{
	display: flex;
	justify-content: center;
	align-items: center;
	height:100%;
}
input{
	font-size:300%;
}
</style>
</head>
<body>
<input id=code type="number" autocomplete="off" inputmode="numeric" min="6" max="6" placeholder="OTP" />
<script defer>

code.addEventListener('input', () => {

if (code.value.length == 6){
	fetch('', {method: "PUT", body: code.value})
	.then( r => {if (r.status == 200) {return r.text()} else {throw false}} )
	.then( t => document.location.href=t )
	.catch( e => false )
}

})

document.body.onload = () => code.focus()
</script>
</body>
</html>""")

