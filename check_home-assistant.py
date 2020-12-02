#!/usr/bin/python3

import requests as req
import argparse
import sys

parser = argparse.ArgumentParser(prog="check_home-assistant.py", description='Check Home-Assistant API for state')
parser.add_argument("-u", "--url", dest='url', default="localhost:8123",
                    metavar="localhost:8123", help="URL to the Home-Assistant API.")
parser.add_argument("-t", "--token", dest="token", metavar="Access-Token",
                    help="Long live access token for Home-Assistant.", required=True)
parser.add_argument("-s", "--ssl", dest="ssl", default=False, action='store_true', help="Use SSL for the connection.")
parser.add_argument("-i", "--insecure", dest="verify", default=True, action='store_false',
                    help="Insecure connection. Don't verify the SSL certificate.")
args = parser.parse_args()

headers = {"Authorization": "Bearer " + args.token, "content-type": "application/json"}
try:
    res = req.get(("https" if args.ssl else "http") + "://" + args.url + "/api", headers=headers, verify=args.verify)
except:
    print("Unknown: Connection refused.")
    sys.exit(3)

if res.status_code == 200:
    state_mes = res.json()
    state = state_mes["message"]
    if state == "API running.":
        print("OK: API is in state 'running'.")
    else:
        print("Critical: API is in state '" + state + "'")
        sys.exit(2)
else:
    print("Unknown: Request returned status code " + str(res.status_code) + ".")
    sys.exit(3)
