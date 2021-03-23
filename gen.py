#!/usr/bin/env python3
import sys
import random

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
for x in range(16):
	sys.stdout.write( random.choice(alphabet) )