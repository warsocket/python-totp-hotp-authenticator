#!/usr/bin/env python3
import authenticator
import os
import sys
import json
import time

authgen = os.path.join(BASE_DIR, "otp.json")
try:
	with open(authgen, "r") as f:
		obj = json.load(f)

except FileNotFoundError:
	obj = {"sessionlength": 900, "secret": "secretsecretsecretsecret", "lastcode": None, "laststamp": None}

	with open(authgen, "w") as f:
		json.dump(obj, f)

compare_code = authenticator.totp(obj["secret"])
sys.stdin.readline()
input_code = sys.stdin.readline().strip()

if compare_code == input_code: # new code accepted
	obj["lastcode"] = compare_code
	obj["laststamp"] = int(time.time())
elif (input_code == obj["lastcode"]) and ((time.time()-obj["sessionlength"]) < obj["laststamp"]):
	pass
else:
	sys.exit(1)

with open(authgen, "w") as f:
	json.dump(obj, f)

# sys.exit(int(compare_code != input_code)) #0=true 1=false