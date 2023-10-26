"""
CustomHTTPError module

This module provides the CustomHTTPError class, which represents a custom HTTP error.
It can be used to raise custom exceptions with specific HTTP status codes and response text.

Classes:
    CustomHTTPError
"""


class CustomHTTPError(Exception):
    """
    Represents a custom HTTP error.

    This exception class is used to raise custom HTTP errors with
    specific status codes and response text.
    It inherits from the base Exception class.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        response_text (str): The text or message associated with the error response.

    Methods:
        __init__(self, status_code, response_text):
            Initializes a new instance of the CustomHTTPError class.
            Args:
                status_code (int): The HTTP status code associated with the error.
                response_text (str): The text or message associated with the error response.
            Returns:
                None.
    """

    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"HTTP Error {status_code}: {response_text}")
