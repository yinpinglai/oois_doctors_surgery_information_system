class UnauthenticatedException(Exception):
    '''
    Unauthenticated Exception raised for errors when user has not authenticated yet

    Attributes:
        message - explanation of the error
    '''
    def __init__(self, message='User unauthenticated') -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
