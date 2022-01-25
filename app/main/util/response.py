from typing import Dict

def produce_common_response_dict(is_success: bool, message: str = '', payload: object = None) -> Dict[str, str]:
	'''
	produce a common response dictionary
	:param: is_success:

	:return: Dictionary
	'''
	response_object = {
		'is_success': is_success
	}
	if message != '':
		response_object['message'] = message

	if payload is not None:
		response_object['payload'] = payload

	return response_object

