"""
This module contains an object that represents the base class for interacting
with the WhatsappCloud API
"""

import os
from dotenv import load_dotenv

load_dotenv()


# pylint: disable=too-few-public-methods
class _BaseApi:
    # pylint: disable=line-too-long

    """
    Base class for interacting with the WhatsApp API.

    This class provides essential configuration and authentication parameters for making requests
    to the WhatsApp API. It is meant to be inherited by other classes that will implement
    specific bot functionality.

    Attributes:
        WA_URL (str): The base URL for WhatsApp API requests, including the API version
        and phone number ID.
        HEADERS (dict): HTTP headers for API requests, including "Content-Type" and "Authorization" with the
        Cloud API access token.
    """

    __cloud_api_access_token = os.getenv("CLOUD_API_ACCESS_TOKEN")
    __wa_phone_number_id = os.getenv("WA_PHONE_NUMBER_ID")
    __version = os.getenv("WA_VERSION")
    WA_URL = f"https://graph.facebook.com/{__version}/{__wa_phone_number_id}/messages"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {__cloud_api_access_token}",
    }

    def __init__(
        self,
        cloud_api_access_token: str = None,
        wa_phone_number_id: str = None,
        version: str = "v17.0",
    ):
        """
        Initialize the BaseApi instance.

        Args:
            cloud_api_access_token (str, optional): The Cloud API access token used for authentication,
            if not provided it is replaced with the one defined in the environment variables .
            wa_phone_number_id (str, optional): The WhatsApp phone number ID,
            if not provided it is replaced with the one defined in the environment variable.
            version (str, optional): The WhatsApp API version to use. Default is "v17.0",
            if not provided it is replaced with the one defined in the environment variable.

        Raises:
            RuntimeError: If neither `cloud_api_access_token` nor `wa_phone_number_id` is provided, and
            there are no corresponding environment variables set, a `RuntimeError` is raised.
        """

        if not cloud_api_access_token:
            cloud_api_access_token = (self.__cloud_api_access_token,)

        if not wa_phone_number_id:
            wa_phone_number_id = (self.__wa_phone_number_id,)

        if not version:
            version = self.__version

        if not cloud_api_access_token or not wa_phone_number_id:
            raise RuntimeError(
                "Either pass in your CLOUD_API_ACCESS_TOKEN or WA_PHONE_NUMBER_ID, "
                "Or place it in your env file"
            )

        self.__cloud_api_access_token = cloud_api_access_token
        self.__wa_phone_number_id = wa_phone_number_id
        self.__version = version
