import argparse
from sseclient import SSEClient


"""
> This function is request api sse service.
api - subscribe
"""

parser = argparse.ArgumentParser(
    description='Subscribe to the channel to receive messages')
parser.add_argument('--channel', type=str, default='channel',
                    help='channel name to receive messages')
args = parser.parse_args()

URL_PREFIX = "http://localhost:8000/sse"
HEADERS = {"Authorization": "Token E9kxMWQSsRprr7w8gbnWKgMmpsVfGfJ6+rBINx4/QCk63LXSOrfZX38lR6KmLqrRa56B1rNMTaSQZp1BsAB2Rg=="
           }

messages = SSEClient(
    f"{URL_PREFIX}/subscribe/?channel={args.channel}", headers=HEADERS)
for msg in messages:
    outputMsg = msg.data
    print(outputMsg)
