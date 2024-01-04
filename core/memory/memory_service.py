from core.lib_fastapi.view_header import *


class MemoryService():
    def __init__(self, time_disable_subscribe: int = 180, **kwargs: Any) -> None:
        self.store = {}
        self.time_disable_subscribe = time_disable_subscribe

    # Memory Stream
    def set_stream(self, key: str, fields: str):
        """
        > This function sets the stream data into memory
        :param
            key: The key of the stream
            fields: The fields of the stream
        :return True
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                self.store[key] = [fields]
                return True

            self.store[key].append(fields)

            return True
        except Exception as e:
            logging.error(
                f"[MemoryService] set_stream : Cannot set stream data into memory : {e}.")
            return

    def get_stream(self, key: str):
        """
        > This function gets a field and value in a stream stored at key
        :param
            key: The key of the stream
        :return Dict or None
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                return None
            else:
                result = self.store[key][-1]
                return result
        except Exception as e:
            logging.error(
                f"[MemoryService] get_stream : Cannot get stream data from memory : {e}.")
            return

    # Memory List
    def set_list(self, key: str, fields: str):
        """
        > This function sets the list data into memory
        :param
            key: The key of the list
            fields: The fields of the list
        :return True
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                self.store[key] = [fields]
                return True

            self.store[key].append(fields)

            return True
        except Exception as e:
            logging.error(
                f"[MemoryService] set_list : Cannot set list data into memory : {e}.")

    def del_list_field(self, key: str, field: str):
        """
        > This function deletes a field in a list stored at key
        :param
            key: The key of the list
            field: The fields of the list
        :return True or None
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                return True

            if field in self.store[key]:
                self.store[key].remove(field)
                return True

            return None
        except Exception as e:
            logging.error(
                f"[MemoryService] del_list_field : Cannot delete a field in list stored from memory : {e}.")

    def del_list(self, key: str):
        """
        > This function deletes the list from memory
        :param
            key: The key of the list
        :return True or None
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                return None

            del self.store[key]

            return True
        except Exception as e:
            logging.error(
                f"[MemoryService] del_list : Cannot delete list from memory : {e}.")
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
            if self.store.get(key) is None or self.store.get(key) == []:
                return None

            if field in self.store[key]:
                return True

            return None
        except Exception as e:
            logging.error(
                f"[MemoryService] find_list_field : Cannot find a field in list stored from memory : {e}.")
            return

    def get_len_list(self, key: str):
        """
        > This function gets length the list stored at key
        :param
            key: The key of the list
        :return len() or None
        """
        try:
            if self.store.get(key) is None or self.store.get(key) == []:
                return 0
            elif self.store.get(key) is not None:
                return len(self.store[key])

            return None
        except Exception as e:
            logging.error(
                f"[MemoryService] get_len_list : Cannot get length the list stored from memory : {e}.")
            return

    # Memory Temp
    def set_temp(self, key: str, fields: str, temp: list = []):
        """
        > This function sets the temp data into memory
        :param
            key: The key of the temp
            fields: The fields of the temp
            temp: The temp is list
        :return True or None
        """
        try:
            if temp == []:
                temp.append({key: [fields]})
                return True
            if self.find_temp_field(key, fields, temp) is None:
                found_key = False
                for item in temp:
                    if key in item:
                        item[key].append(fields)
                        found_key = True
                        return True
                if found_key == False:
                    temp.append({key: [fields]})
                    return True
                
            return None
        except Exception as e:
            logging.error(
                f"[MemoryService] set_temp : Cannot set temp data into memory : {e}.")
            return

    def find_temp_field(self, key: str, field: str, temp: list):
        """
        > This function find a field in a temp stored at key
        :param
            key: The key of the temp
            field: The field of the temp
            temp: The temp is list
        :return True or None
        """
        try:
            for item in temp:
                if key in item:
                    if field in item[key]:
                        return True
            return None
        except Exception as e:
            logging.error(
                f"[MemoryService] find_temp_field : Cannot find a field in temp stored from memory : {e}.")
            return

    def get_message(self, key: str, temp: list):
        """
        > This function gets message the temp stored at key
        :param
            key: The key of the temp
            temp: The temp is list
        :return Str or None
        """
        try:
            for item in temp:
                if self.store.get(key) is None or self.store.get(key) == []:
                    return None
                else:
                    result = item[key][-1]
                    return str(result)
        except Exception as e:
            logging.error(
                f"[MemoryService] get_message : Cannot get message in temp stored from memory : {e}.")
            return
        