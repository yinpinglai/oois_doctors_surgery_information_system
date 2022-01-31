from datetime import date, datetime

class DateTimeUtil:

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

