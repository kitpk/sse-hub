from core.redis.redis_service import RedisService
from ..utils.util_datetime import Datetime as conf_date
from core.lib_fastapi.view_header import *
import redis
import aioredis

import os
from dotenv import load_dotenv
load_dotenv()


class RedisPubSub(RedisService):
    def __init__(self, time_disable_subscribe: int = 180, **kwargs: Any) -> None:
        self.redis = redis.from_url(os.getenv('REDIS_URL'))
        self.aioredis = aioredis.from_url(os.getenv('REDIS_URL'))
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
            logging.error(f"[RedisPubSub] connect : {e}")
            return None

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
            logging.error(f"[RedisPubSub] disconnect : {e}")
            return None

    async def publish(self, request: Request, channel: str, message: str = ""):
        try:
            pub_key = 'Pub_' + channel
            fields = {"time": str(datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S.%f")[:-4]), "channel": channel, "message": message}
            result = self.set_stream(pub_key, fields)
            if result is None:
                return None
            await self.aioredis.publish(pub_key, str(fields))

            return fields
        except Exception as e:
            logging.error(f"[RedisPubSub] publish : {e}")
            return None

    async def subscribe(self, request: Request, channel: str):
        try:
            pubsub = self.aioredis.pubsub()
            async with pubsub as sub:
                pub_key = 'Pub_' + channel
                # If the server never activates the channel is channel not found
                result = self.get_stream(pub_key)
                if result is None:
                    yield 'data: ' + str({"message": "Channel not found"})
                    raise Exception(str({"message": "Channel not found"}))

                # If the server is disable channel for more than 3 minutes is channel not found
                byte_last_data = {y.decode('ascii'): result.get(
                    y).decode('ascii') for y in result.keys()}
                _, last_data = conf_date.str2datetime(byte_last_data["time"])
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

                self.STOP = False
                await sub.subscribe(pub_key)
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
                            raise Exception(
                                str({"message": "Disconnect failed"}))
                        yield 'data: ' + str({"message": "The server stopped sending data for more than 3 minutes"})
                        break

                    try:
                        async with async_timeout.timeout(1):
                            message = await sub.get_message(ignore_subscribe_messages=True)
                            if message is not None:
                                yield 'data: ' + str({"message": message['data'].decode("utf-8")}) + '\n'
                                start_time = datetime.utcnow()
                            await asyncio.sleep(0.1)
                    except:
                        result = self.disconnect(request, channel)
                        if result is None:
                            raise Exception(
                                str({"message": "Disconnect failed"}))
                        yield 'data: ' + str({"message": "Disconnect success"})
                        break

                if self.STOP:
                    yield 'data: ' + str({"message": f"Server Disable channel {channel} success"})

        except Exception as e:
            logging.error(f"[RedisPubSub] subscribe : {e}")

    async def disable_subscribe(self, request: Request, channel: str):
        try:
            self.STOP = True
            sub_key = 'Sub_' + channel
            result = self.del_list(sub_key)
            if result is None:
                raise Exception(
                    {"message": f"Disable channel {channel} failed"})

            return {"message": f"Disable channel {channel} success"}
        except Exception as e:
            logging.error(f"[RedisPubSub] disable_subscribe : {e}")
            return {"message": f"Disable channel {channel} failed"}
