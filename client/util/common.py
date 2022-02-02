from typing import Dict


class CommonUtil:

    @staticmethod
    def construct_request_headers(token: str) -> Dict:
        return {
            'Authorization': token,
        }

