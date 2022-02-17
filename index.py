#!/usr/bin/env python3
import sys
from urllib.parse import parse_qsl
sys.path.append("/var/www")
from session import authed, authredirect

if not authed(): authredirect()

print("Content-Type: text/plain\r\n\r")
print("You are logged in")
