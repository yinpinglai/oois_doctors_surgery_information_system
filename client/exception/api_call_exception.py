class ApiCallException(Exception):
    '''
    API Call Exception raised for errors generated from the API response

    Attributes:
        message - explanation of the error
    '''
    def __init__(self, message='') -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

