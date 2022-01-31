from typing import Dict, Any
from abc import ABCMeta, abstractmethod


class JSONSerializable(metaclass=ABCMeta):

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        '''
        Serializes the object instance to the JSON standard format

        :return serialized_dictionary - The serialized JSON dictionary
        '''
        pass

