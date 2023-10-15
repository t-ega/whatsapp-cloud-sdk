from pydantic import BaseModel
from typing import Callable

"""
This file defines the Pydantic model used for validating a callback function
"""


class Webhook(BaseModel):
    """
    Represents a webhook for handling incoming data and calls a provided callback function.

    Args:
        callback (Callable): A callback function to be executed when incoming data is received.

    Attributes:
        callback (Callable): The callback function provided to the webhook.

    Example:

        def my_callback(data):
            # Handle incoming data here.

        webhook = Webhook(callback=my_callback)


    Note:
        The provided `callback` should be a callable function that can handle incoming data.

    See also:
      - :class:`pydantic.BaseModel` The base class for the Webhook class.
    """

    callback: Callable
