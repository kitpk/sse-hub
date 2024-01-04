from core.lib_fastapi.view_header import *
import redis
import aioredis

import os
from dotenv import load_dotenv
load_dotenv()


class RedisService():
    def __init__(self, time_disable_subscribe: int = 180, **kwargs: Any) -> None:
        self.redis = redis.from_url(os.getenv('REDIS_URL'))
        self.aioredis = aioredis.from_url(os.getenv('REDIS_URL'))
        self.time_disable_subscribe = time_disable_subscribe

    # Redis Stream
    def set_stream(self, key: str, fields: str):
        """
        > This function sets the stream data into redis
        :param
            key: The key of the stream
            fields: The fields of the stream
        :return True or None
        """
        try:
            result = self.redis.xadd(name=key, fields=fields)
            if result is None:
                return None

            return True
        except Exception as e:
            logging.error(
                f"[RedisService] set_stream : Cannot set stream data into redis : {e}.")
            return

    def get_stream(self, key: str):
        """
        > This function gets a field and value in a stream stored at key
        :param
            key: The key of the stream
        :return Dict or None
        """
        try:
            result = self.redis.xrevrange(name=key, min="-", max="+", count=1)
            if result == [] or None:
                return None

            return result[0][1]
        except Exception as e:
            logging.error(
                f"[RedisService] get_stream : Cannot get stream data from redis : {e}.")
            return

    # Redis List
    def set_list(self, key: str, fields: str):
        """
        > This function sets the list data into redis
        :param
            key: The key of the list
            fields: The fields of the list
        :return True or None
        """
        try:
            result = self.redis.lpush(key, fields)
            if result is None:
                return None

            return True
        except Exception as e:
            logging.error(
                f"[RedisService] set_list : Cannot set list data into redis : {e}.")
            return

    def del_list_field(self, key: str, field: str):
        """
        > This function deletes a field in a list stored at key
        :param
            key: The key of the list
            field: The fields of the list
        :return True or None
        """
        try:
            result = self.redis.lrem(name=key, count=1, value=field)
            if result is None:
                return None

            return True
        except Exception as e:
            logging.error(
                f"[RedisService] del_list_field : Cannot delete a field in list stored from redis : {e}.")
            return

    def del_list(self, key: str):
        """
        > This function deletes the list from redis
        :param
            key: The key of the list
        :return True or None
        """
        try:
            count = self.get_len_list(key)
            result = self.redis.lpop(name=key, count=count)
            if result is None:
                return None

            return True
        except Exception as e:
            logging.error(
                f"[RedisService] del_list : Cannot delete list from redis : {e}.")
            return

    def find_list_field(self, key: str, field: str):
        """
        > This function find a field in a list stored at key
        :param
            key: The key of the list
            field: The fields of the list
        :return True or None
        """
        try:
            result = self.redis.lpos(name=key, value=field)
            if result is None:
                return None

            return True
        except Exception as e:
            logging.error(
                f"[RedisService] find_list_field : Cannot find a field in list stored from redis : {e}.")
            return

    def get_len_list(self, key: str):
        """
        > This function gets length the list stored at key
        :param
            key: The key of the list
        :return len() or None
        """
        try:
            result = self.redis.llen(key)
            if result is None:
                return None

            return result
        except Exception as e:
            logging.error(
                f"[RedisService] get_len_list : Cannot get length the list stored from redis : {e}.")
            return
