import time
import subprocess


class Test():
    """
    > This script is used to run the tests sse service
    :Test - Channel not found case scenario
    :Test - Waiting server sent message case scenario
    :Test - Multi client case scenario
    """

    fake_channel1 = "Ch_test1"
    fake_channel2 = "Ch_test2"

    def Test_channel_not_found(self):
        """
        > This function
        :Test - Channel not found scenario
        """
        try:
            print("========Server========")
            print("========Client========")
            client1 = self.api_client(self.fake_channel1)
            client1.wait(1)
        except subprocess.TimeoutExpired:
            time.sleep(1)
            client1.kill()

    def Test_waiting_server_sent_message(self):
        """
        > This function
        :Test - Waiting server sent message
        """
        try:
            print("========Server========")
            self.api_server(self.fake_channel1,
                            f"Server Connect in {self.fake_channel1}")
            print("========Client========")
            client1 = self.api_client(self.fake_channel1)
            client1.wait(6)
        except subprocess.TimeoutExpired:
            time.sleep(1)
            client1.kill()

    def Test_multi_client(self):
        """
        > This function
        :Test - Multi client case scenario
        """
        try:
            print("========Server========")
            self.api_server(self.fake_channel1,
                            f"Server Connect in {self.fake_channel1}")
            client1 = self.api_client(self.fake_channel1)
            time.sleep(0.5)
            self.api_server(self.fake_channel1, "Channel_Test 1")
            self.api_server(self.fake_channel1, "Data 1")
            self.api_server(self.fake_channel1, "Data 2")
            print("----------------------")
            time.sleep(0.5)
            self.api_server(self.fake_channel2,
                            f"Server Connect in {self.fake_channel2}")
            client2 = self.api_client(self.fake_channel2)
            time.sleep(0.5)
            self.api_server(self.fake_channel2, "Channel_Test 2")
            self.api_server(self.fake_channel2, "Data 3")
            client1.wait(1)
        except subprocess.TimeoutExpired:
            self.api_server_disable(self.fake_channel1)
            print("========Client========")
            time.sleep(1)
            client1.kill()

            self.api_server_disable(self.fake_channel2)
            time.sleep(1)
            client2.kill()

    def api_server_disable(self, channel: str):
        subprocess.run(["python", "tests/test_disable.py",
                        "--channel", f"{channel}"])

    def api_client(self, channel: str):
        client = subprocess.Popen(["python", "tests/test_subscribe.py",
                                   "--channel", f"{channel}"])
        return client

    def api_server(self, channel: str, message: str):
        print(f'publish <"{channel}"> <"{message}">')
        server = subprocess.run(["python", "tests/test_publish.py",
                                "--channel", f"{channel}", "--message", f"{message}"])


if __name__ == "__main__":
    t = Test()
    print("Start Testing\n")
    print("Test 1 - Channel not found case scenario")
    Test_1 = t.Test_channel_not_found()
    print("\nTest 2 - Waiting server sent message case scenario")
    Test_2 = t.Test_waiting_server_sent_message()
    print("\nTest 3 - Multi client case scenario")
    Test_3 = t.Test_multi_client()
    print("\nEnd Testing")
