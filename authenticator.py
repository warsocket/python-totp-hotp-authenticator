#!/usr/bin/env python3
import base64
import struct
import hmac
from hashlib import sha1
from time import time

def safeb32decode(data):
	if ((len(data) * 5 ) % 8) >= 5: data = data[:-1] #last character encodes no new byte
	padcount = (8-(len(data)%8))%8 #calculate padding
	data += "="*padcount
	return(base64.b32decode(data, True))


def timestampgeneration(): 
	return int(time()) // 30


def otp(secret, generation=timestampgeneration()):
	digest = hmac.new(
		safeb32decode(secret),
		struct.pack("!Q", generation),
		sha1
		).digest()

	index = digest[19] & 0xF
	number = (struct.unpack("!I", digest[index:index+4])[0] & 0x7FFFFFFF) % 10**6
	return "{:0>6}".format(number)

def hotp(secret, generation):
	return otp(secret, generation)

def totp(secret):
	return otp(secret)


# print(totp("SECRETSECRETSECRET")) #this will print the google auth timed code for the secret "SECRETSECRETSECRET"
