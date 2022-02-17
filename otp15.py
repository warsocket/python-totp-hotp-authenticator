#!/usr/bin/env python3
import sys

from authenticator import otp, timestampgeneration
with open("/var/www/secret", "r") as f: secret = f.read().rstrip()

gen = timestampgeneration()

candidates = set(
	map(
		lambda x: otp(secret, gen-x), 
		range(31) #current slot + 30 * 30 s back = 15 mins
	)
)

username = sys.stdin.readline()
password = sys.stdin.readline().rstrip()

sys.exit( int(password not in candidates) )