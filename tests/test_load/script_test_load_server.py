import time
import asyncio
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Script test load server')
parser.add_argument('--topic', type=int, default=1,
                    help='len(topic)')
args = parser.parse_args()


class Test_load_performance():
    """
    > This script is used to run the tests load performance sse service.
    :params 
        topic: len(topic)
    :Test - :client per :topic how CPU Usage(%) and Memory Usage(%)
    """

    def test_load(self, topic: int):
        asyncio.ensure_future(self.server(topic))
        loop = asyncio.get_event_loop()
        loop.run_forever()

    async def server(self, number: int):
        c = f"Ch_test{number}"
        self.api_server(c, f"Server Connect in {c}")
        for send in range(50000):
            await asyncio.sleep(0)
            self.api_server(c, f"Data {send}")

    def api_server(self, channel: str, message: str):
        print(f'publish <"{channel}"> <"{message}">')
        server = subprocess.run(["python", "tests/test_publish.py",
                                "--channel", f"{channel}", "--message", f"{message}"])


if __name__ == "__main__":
    t = Test_load_performance()
    t.test_load(args.topic)
