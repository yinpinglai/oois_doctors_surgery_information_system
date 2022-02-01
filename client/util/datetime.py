from dateutil import parser
from datetime import datetime


class DateTimeUtil:

    @staticmethod
    def from_iso_datetime_string(iso8601_datetime_string: str) -> datetime:
        '''
        Converts the ISO8601 datetime string to the datetime type of Python object

        :param iso8601_datetime_string - The ISO8601 datetime string
        :return datetime_instance - The datetime instance after parsed from the ISO8601 datetime string
        '''
        datetime_instance = parser.parse(iso8601_datetime_string)
        return datetime_instance

