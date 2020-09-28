#!/usr/bin/python3

import asyncio
import json
import asyncws
import argparse

parser = argparse.ArgumentParser(prog="check_mailcow.py", description='Check Home-Assistant API for state')
parser.add_argument("-u", "--url", dest='url', default="localhost:8123",
                    metavar="localhost:8123", help="URL to the Home-Assistant API.")
parser.add_argument("-t", "--token", dest="token", metavar="Access-Token",
                    help="Long live access token for Home-Assistant.", required=True)
args = parser.parse_args()


async def main():
    """Simple WebSocket client for Home Assistant."""
    websocket = await asyncws.connect("ws://" + args.url + "/api/websocket")
    await websocket.recv()

    await websocket.send(json.dumps(
        {'type': 'auth',
         'access_token': args.token}
    ))
    await websocket.recv()

    await websocket.send(json.dumps(
        {'id': 1, 'type': 'system_health/info'}
    ))

    message = await websocket.recv()
    message = json.loads(message)
    if message is not None:
        if "result" in message.keys():
            if "homeassistant" in message['result'].keys():
                if "version" in message['result']['homeassistant'].keys():
                    print("OK: Home-Assistant version " + message['result']['homeassistant']['version'])
                else:
                    print("Critical: missing key 'version'.")
            else:
                print("Critical: missing key 'homeassistant'.")
        else:
            print("Critical: missing key 'result'.")
    else:
        print("Critical: got no response.")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
