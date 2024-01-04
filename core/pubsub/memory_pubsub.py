from core.memory.memory_service import MemoryService
from ..utils.util_datetime import Datetime as conf_date
from core.lib_fastapi.view_header import *
import asyncio
import async_timeout


class MemoryPubSub(MemoryService):
    def __init__(self, time_disable_subscribe: int = 180, **kwargs: Any):
        self.store = {}
        self.time_disable_subscribe = time_disable_subscribe

    def ping(self, request: Request):
        return {"ping": "pong!"}

    def connect(self, request: Request, channel: str):
        try:
            sub_key = 'Sub_' + channel
            access_token = request.headers.get('Authorization', None)
            if access_token is not None:
                head, token = access_token.split(" ")
            result = self.set_list(sub_key, token)
            if result is None:
                return None
            return True
        except Exception as e:
            logging.error(f"[MemoryPubSub] connect : {e}")
            return

    def disconnect(self, request: Request, channel: str):
        try:
            sub_key = 'Sub_' + channel
            access_token = request.headers.get('Authorization', None)
            if access_token is not None:
                head, token = access_token.split(" ")
            if self.find_list_field(sub_key, token):
                result = self.del_list_field(sub_key, token)
                if result is None:
                    return None
                return True
            return None
        except Exception as e:
            logging.error(f"[MemoryPubSub] disconnect : {e}")
            return None

    def publish(self, request: Request, channel: str, message: str = ""):
        try:
            pub_key = 'Pub_' + channel
            fields = {"time": str(datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S.%f")[:-4]), "channel": channel, "message": message}
            result = self.set_stream(pub_key, fields)
            if result is None:
                return None
            try:
                self.set_temp(pub_key, fields, self.temp)
            except:
                self.set_temp(pub_key, fields)

            return fields
        except Exception as e:
            logging.error(f"[MemoryPubSub] publish : {e}")
            return None

    async def subscribe(self, request: Request, channel: str):
        try:
            pub_key = 'Pub_' + channel
            # If the server never activates the channel is channel not found
            result = self.get_stream(pub_key)
            if result is None:
                yield 'data: ' + str({"message": "Channel not found"})
                raise Exception(str({"message": "Channel not found"}))
            
            # If the server is disable channel for more than 3 minutes is channel not found
            _, last_data = conf_date.str2datetime(result["time"])
            time_last_data = (datetime.utcnow() -
                              last_data).total_seconds()
            if (time_last_data >= self.time_disable_subscribe):
                yield 'data: ' + str({"message": "Channel not found"})
                raise Exception(str({"message": "Channel not found"}))

            # If client connect not success is connect failed
            result = self.connect(request, channel)
            if result is None:
                yield 'data: ' + str({"message": "Connect failed"})
                raise Exception(str({"message": "Connect failed"}))

            self.temp = []
            previous_message = None

            self.STOP = False
            sub_key = 'Sub_' + channel
            len_client = self.get_len_list(sub_key)
            yield 'data: ' + str(f"Welcome SSE HUB in channel {channel}") + '\n'
            start_time = datetime.utcnow()

            while False if (self.STOP == True) and (len_client == 0) else True:
                len_client = self.get_len_list(sub_key)

                # If the server stopped sending data for more than 3 minutes, client disconnect
                time = (datetime.utcnow() - start_time).total_seconds()
                if (time >= self.time_disable_subscribe):
                    result = self.disconnect(request, channel)
                    if result is None:
                        raise Exception(str({"message": "Disconnect failed"}))
                    yield 'data: ' + str({"message": "The server stopped sending data for more than 3 minutes"})
                    break

                try:
                    async with async_timeout.timeout(1):
                        message = self.get_message(pub_key, self.temp)
                        if message is not None:
                            if previous_message != message:
                                yield 'data: ' + str({"message": message}) + '\n'
                                start_time = datetime.utcnow()
                                previous_message = message
                        await asyncio.sleep(0.1)
                except:
                    result = self.disconnect(request, channel)
                    if result is None:
                        raise Exception(str({"message": "Disconnect failed"}))
                    yield 'data: ' + str({"message": "Disconnect success"})
                    break

            if self.STOP:
                yield 'data: ' + str({"message": f"Server Disable channel {channel} success"})

        except Exception as e:
            logging.error(f"[MemoryPubSub] subscribe : {e}")

    def disable_subscribe(self, request: Request, channel: str):
        try:
            self.STOP = True
            sub_key = 'Sub_' + channel
            result = self.del_list(sub_key)
            if result is None:
                raise Exception(
                    {"message": f"Disable channel {channel} failed"})

            return {"message": f"Disable channel {channel} success"}
        except Exception as e:
            logging.error(f"[MemoryPubSub] disable_subscribe : {e}")
            return {"message": f"Disable channel {channel} failed"}

    def get_data_stream(self, request: Request):
        return self.store

    def get_data_temp(self, request: Request):
        return self.temp
