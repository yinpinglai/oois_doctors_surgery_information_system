import time
from dateutil import parser
from datetime import date, datetime

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

    @staticmethod
    def serialize_datetime_object(datetime_instance: datetime) -> str:
        '''
        Serializes the datetime object to the JSON format

        :param datetime_instance - The datetime instance to be serialized
        :return serialized_datetime_instance - The serialize datetime instance JSON string
        '''

        if isinstance(datetime_instance, (datetime, date)):
            return datetime_instance.isoformat()

        return datetime_instance

    @staticmethod
    def to_local_timezone(utc_datetime_instance: datetime) -> datetime:
        '''
        Converts the UTC datetime instance to the local timezone

        :param datetime_instance - The datetime instance to be converted
        :return localized_datetime_instance - The localized datetime instance
        '''
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime_instance + offset
