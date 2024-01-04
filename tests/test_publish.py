import argparse
import requests


"""
> This function is request api sse service.
api - publish
"""

parser = argparse.ArgumentParser(description='Publish message into channel')
parser.add_argument('--channel', type=str, default='channel',
                    help='channel name to send')
parser.add_argument('--message', type=str,
                    default='message', help='message to send')
args = parser.parse_args()

URL_PREFIX = "http://localhost:8000/sse"
HEADERS = {"Authorization": "Token E9kxMWQSsRprr7w8gbnWKgMmpsVfGfJ6+rBINx4/QCk63LXSOrfZX38lR6KmLqrRa56B1rNMTaSQZp1BsAB2Rg==",
           "SSE-SERVER-KEY": "eyJhbGciOiJIUzI1NiJ9.e30.WRPIcX2KjS4BcseZpEo-G5HI_ae6oWKvWprgV4_PheY"}

server = requests.get(
    f"{URL_PREFIX}/publish/?channel={args.channel}&message={args.message}", headers=HEADERS)
