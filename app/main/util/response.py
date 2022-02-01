from typing import Dict, Any
from app.main.model.json_serializable import JSONSerializable

class ResponseUtil:

    @staticmethod
    def produce_common_response_dict(is_success: bool, message: str = '', payload: object = None) -> Dict[str, str]:
        '''
        produce a common response dictionary
        :param: is_success - The indicator of the response
        :param message - (Optional) The message to be returned
        :param payload - (Optional) The payload to be returned

        :return: Dictionary - The common response dictionary
        '''
        response_object = {
            'is_success': is_success
        }
        if message != '':
            response_object['message'] = message

        if payload is not None:
            response_object['payload'] = payload

        return response_object


    @staticmethod
    def convert_to_json_serializable(serializable_instance: Any) -> Any:
        '''
        Converts the list of iterable to a JSON list

        :param serializable_instance - A JSON serializable instance

        :return serialized_instance - The serialized JSON instance with corresponding data type
        '''
        if serializable_instance is None:
            return serializable_instance

        if isinstance(serializable_instance, list):
            result_list = []

            for data in serializable_instance:
                if type(data) is JSONSerializable:
                    result_list.append(data.serialize())
                else:
                    result_list.append(data)

            return result_list
        elif type(serializable_instance) is JSONSerializable:
            return serializable_instance.serialize()
        else:
            return serializable_instance

