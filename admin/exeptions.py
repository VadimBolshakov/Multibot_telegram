from typing import Optional


class ResponseStatusError(Exception):
    """Exception raised for errors in the response status get or post method.

    Attributes:
        param -- input parameter which caused the error
        msg -- explanation of the error.
    """

    def __init__(self, param: Optional[int] = None, msg: str = 'An unknown error occurred'):
        self.param: int = param
        self.message: str = msg
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.param:
            self.message = str(f'Response status {self.param} error')
        return self.message


class ResponseStatusNewsAPIError(Exception):
    """Exception raised for errors in the response status from newsapi.

    Attributes:
        param -- input parameter which caused the error (get from response['code'])
        msg -- explanation of the error (get from response['message']).
    """

    def __init__(self, param: Optional[str] = None, msg: str = 'An unknown error occurred'):
        self.param: str = param
        self.message: str = msg
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.param:
            self.message = str(f'Response status NewsAPI {self.param} error. {self.message}')
        return self.message


class ResponseTotalResultsNewsAPIError(Exception):
    """Exception raised for null in the response totalResults from newsapi.

    Attributes:
        msg -- explanation of the error.
    """

    def __init__(self, msg: str = 'Total results is null from NewsAPI'):
        self.message: str = msg
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
