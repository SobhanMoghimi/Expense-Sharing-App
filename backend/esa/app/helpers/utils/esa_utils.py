import datetime
import logging
import random
import string
import uuid
import os
from typing import List

class CommonsUtils:
    @classmethod
    def all_base_classes(cls, clazz):
        base_class_set = set(clazz.__bases__)
        all_base_class_set = set({clazz})
        all_base_class_set.update(base_class_set)
        for base in base_class_set:
            all_base_class_set.update(cls.all_base_classes(base))
        return all_base_class_set

    @classmethod
    def walk_all_parent_dirs(cls, path: str) -> List[str]:
        # type: (Text) -> Iterator[Text]
        """
        Yield directories starting from the given directory up to the root
        """
        if not os.path.exists(path):
            raise IOError('Starting path not found')

        if os.path.isfile(path):
            path = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir

class ESAUtils:

    @staticmethod
    def convert_datetime_to_str(datetime_obj: datetime) -> str:
        return format(datetime_obj, '%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def convert_str_to_datetime(datetime_str):
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')

    @classmethod
    def create_nonce(cls) -> str:
        nonce: str = uuid.uuid4().hex.__str__()
        return nonce

    @classmethod
    def create_random_str(cls, min_length: int, max_length: int):
        """
         create a random string with the length of between max_length and min_length
         This random string contains characters of a-z A-Z 0-9
        """
        characters: list = list(string.ascii_letters[:])
        characters.extend(string.digits)
        random_str: str = ""
        random_str_length = random.randint(min_length, max_length)
        for _ in range(0, random_str_length):
            random_index: int = random.randint(0, len(characters) - 1)
            random_str = random_str + characters[random_index]

        return random_str

    @staticmethod
    def handle_exception(e):
        logging.exception(e)

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
