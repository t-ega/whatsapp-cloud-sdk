"""This module Represents a WhatsApp bot for communication with the WhatsApp API."""

from typing import Optional, List, Dict
from unicodedata import decimal
import json
import requests

from _exceptions.http_error import CustomHTTPError
from _base_api import _BaseApi
from _files.contact import Contact
from _utils.json_serializer import MyEncoder
from _validators.messages import (
    TextMessage,
    ButtonMessage,
    ButtonContents,
    LinkMessage,
    LocationMessage,
)

from _formaters.message_formatter import MessageFormatter, LinkTypes


formatter = MessageFormatter()


class Bot(_BaseApi):
    # pylint: disable=line-too-long
    """
    Represents a WhatsApp bot for communication with the WhatsApp API.

    This class inherits from the `BaseApi` class and provides methods for sending various types of
    messages, marking messages as read, and handling communication with the WhatsApp API.

    Args:
        cloud_api_access_token (str, optional): The Cloud API access token used for authentication.
        wa_phone_number_id (str, optional): The WhatsApp phone number ID.
        version (str, optional): The WhatsApp API version to use.

    Inherits attributes from the `BaseApi` class, such as `WA_URL` and `HEADERS`.

    Attributes:
        Inherits attributes from the `BaseApi` class.

    Methods:
        - `send_text(text: str, recipient_number: str, message_id: str = None, preview_url: bool = False)`:
          Send a text message to a recipient.

        - `send_text_with_buttons(text: str, buttons: list, recipient_number: str)`:
          Send a text message with buttons to a recipient.

        - `send_reply_with_reaction(message_id: str, emoji: str, recipient_number: str)`:
          Send a reaction to a message.

        - `send_image_by_url(link: str, caption: Optional[str], recipient_number: str, message_id: Optional[str])`:
          Send an image by URL.

        - `send_audio_by_url(link: str, caption: Optional[str], recipient_number: str)`:
          Send audio by URL.

        - `send_document_by_url(link: str, caption: Optional[str], recipient_number: str)`:
          Send a document by URL.

        - `send_video_by_url(link: str, caption: Optional[str], recipient_number: str, message_id: Optional[str] = None)
        `:
          Send a video by URL.

        - `send_location(latitude: decimal, longitude: int, name: str, address: str, recipient_number: str)`:
          Send a location.

        - `send_contact(contact: list, recipient_number: str)`:
          Send a contact.

        - `send_sticker_with_url(link: str, recipient_number: str)`:
          Send a sticker by URL.

        - `mark_message_as_read(message_id: str)`:
          Mark a message as read.

        - `__send(data: dict, method: Optional[str] = "POST") -> dict`:
          Send data to the WhatsApp API.

    Usage Example:
    ```
    python
    from your_library import Bot

    # Initialize the bot.
    bot = Bot(cloud_api_access_token="your_access_token", wa_phone_number_id="your_phone_number_id", version="v17.0")

    # Use bot methods to interact with the WhatsApp API
    bot.send_text("Hello, world!", "recipient_number")
    ```
    """

    def __init__(
        self,
        cloud_api_access_token: str = None,
        wa_phone_number_id: str = None,
        version: str = None,
    ):
        """
        Initialize a Bot instance for WhatsApp API communication.

        Args:
            cloud_api_access_token (str, optional): The Cloud API access token used for authentication.
            wa_phone_number_id (str, optional): The WhatsApp phone number ID.
            version (str, optional): The WhatsApp API version to use.

        Inherits attributes from the `BaseApi` class.
        """
        super().__init__(
            cloud_api_access_token=cloud_api_access_token,
            wa_phone_number_id=wa_phone_number_id,
            version=version,
        )

    async def send_text(
        self,
        text: str,
        recipient_number: str,
        message_id: str = None,
        preview_url: bool = False,
    ):
        """
        Send a text message to a recipient.

        Args:
            text (str): The text of the message.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): The ID of the message if it is a reply to a message (optional).
            preview_url (bool): Enable or disable URL preview (default is False).

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        message = TextMessage(
            text=text, recipient_number=recipient_number, message_id=message_id
        )

        payload = formatter.format_text_message(
            to=message.recipient_number,
            body=message.text,
            message_id=message_id,
            preview_url=preview_url,
        )
        return await self.__send(data=payload)

    async def send_text_with_buttons(
        self,
        text: str,
        buttons: List[Dict[str, str]],
        recipient_number: str,
        message_id: Optional[str],
    ):
        """
        Send a text message with buttons to a recipient.

        Args:
            text (str): The text of the message.
            buttons (list): List of buttons, where each button is a dictionary with the following keys:

                - 'title' (str): The title or label of the button.
                - 'id' (optional, str): An optional id for the button.

            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        if not isinstance(buttons, list):
            raise TypeError("Buttons must be a list of dict object")

        buttons_content = [ButtonContents(**b) for b in buttons]

        message = ButtonMessage(
            text=text, recipient_number=recipient_number, buttons=buttons_content
        )

        payload = formatter.format_button_message(
            to=recipient_number,
            text=message.text,
            buttons=message.buttons,
            message_id=message_id,
        )

        return await self.__send(data=payload)

    # TODO: Add input validation for all bot methods

    async def send_reaction_message(
        self, message_id: Optional[str], emoji, recipient_number: str
    ):
        """
        Send a reaction message.

        Args:
            message_id (str, optional): An optional message ID if it is a reply to a message.
            emoji (str): The reaction emoji to send.
            recipient_number (str): The recipient's WhatsApp phone number.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        payload = formatter.format_reply_with_reaction(
            to=recipient_number, message_id=message_id, emoji=emoji
        )

        return await self.__send(data=payload)

    async def send_image_by_url(
        self,
        link: str,
        caption: Optional[str],
        recipient_number: str,
        message_id: Optional[str],
    ):
        """
        Send an image by URL to a recipient.

        Args:
            link (str): The URL of the image.
            caption (str, optional): An optional caption for the image.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        message = LinkMessage(link=link, caption=caption)
        payload = formatter.format_link_message(
            to=recipient_number,
            link=message.link,
            m_type=LinkTypes.IMAGE,
            message_id=message_id,
        )
        return await self.__send(data=payload)

    async def send_audio_by_url(
        self,
        link: str,
        recipient_number: str,
        message_id: Optional[str],
    ):
        """
        Send an audio file by URL to a recipient.

        Args:
            link (str): The URL of the audio file.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        message = LinkMessage(link=link)
        payload = formatter.format_link_message(
            to=recipient_number,
            link=message.link,
            m_type=LinkTypes.AUDIO,
            message_id=message_id,
        )
        return await self.__send(data=payload)

    async def send_document_by_url(
        self,
        link: str,
        caption: Optional[str],
        recipient_number: str,
        message_id: Optional[str] = None,
    ):
        """
        Send a document by URL to a recipient.

        Args:
            link (str): The URL of the document.
            caption (str, optional): An optional caption for the document.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """
        message = LinkMessage(
            link=link,
            caption=caption,
        )
        payload = formatter.format_send_document_by_url(
            to=recipient_number,
            document_link=message.link,
            caption=message.caption,
            message_id=message_id,
        )
        return await self.__send(data=payload)

    async def send_video_by_url(
        self,
        link: str,
        caption: Optional[str],
        recipient_number: str,
        message_id: Optional[str] = None,
    ):
        """
        Send a video by URL to a recipient.

        Args:
            link (str): The URL of the video.
            caption (str, optional): An optional caption for the video.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        message = LinkMessage(link=link, caption=caption)
        payload = formatter.format_link_message(
            to=recipient_number,
            link=message.link,
            m_type=LinkTypes.VIDEO,
            caption=message.caption,
            message_id=message_id,
        )

        return await self.__send(data=payload)

    # pylint: disable=too-many-arguments
    async def send_location(
        self,
        latitude: decimal,
        longitude: int,
        name: str,
        address: str,
        recipient_number: str,
        message_id: Optional[str] = None,
    ):
        """
        Send a location to a recipient.

        Args:
            latitude (decimal): The latitude of the location.
            longitude (int): The longitude of the location.
            name (str): The name of the location.
            address (str): The address of the location.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        message = LocationMessage(longitude=longitude, name=name, address=address)

        payload = formatter.format_location_message(
            to=recipient_number,
            name=message.name,
            address=message.address,
            longitude=message.longitude,
            latitude=latitude,
            message_id=message_id,
        )

        return await self.__send(data=payload)

    async def send_contact(
        self,
        contacts: List[Contact],
        recipient_number: str,
        message_id: Optional[str] = None,
    ):
        """
        Send a contact to a recipient.

        Args:
            contacts (list): A list of contact details.Each contact detail a list of contact objects.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        if not isinstance(contacts, list):
            raise TypeError("Contacts must be a list")

        for i, contact in contacts:
            if not isinstance(contact, Contact):
                raise AttributeError(
                    f"Contact {i} must be of type {type(Contact)}. Got {type(type(contact))} instead."
                )

        payload = formatter.format_contact_message(
            contacts=contacts, to=recipient_number, message_id=message_id
        )

        return await self.__send(data=payload)

    async def send_sticker_with_url(
        self,
        link: str,
        recipient_number: str,
        message_id: Optional[str],
    ):
        """
        Send a sticker by URL to a recipient.

        Args:
            link (str): The URL of the sticker.
            recipient_number (str): The recipient's WhatsApp phone number.
            message_id (str, optional): An optional message ID if it is a reply to a message.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        payload = formatter.format_sticker_message_by_url(
            link=link, to=recipient_number, message_id=message_id
        )

        return await self.__send(data=payload)

    async def mark_message_as_read(self, message_id: str):
        """
        Mark a message as read.

        Args:
            message_id (str): The ID of the message to mark as read.

        Raises:
            ValueError: If message_id is not provided.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        if not message_id:
            raise ValueError("A message Id is required")

        payload = formatter.mark_message_as_read(message_id=message_id)
        return await self.__send(data=payload)

    async def __send(
        self,
        data: dict,
    ) -> dict:
        """
        Send data to the WhatsApp API.

        Args:
            data (dict): The data to send to the WhatsApp API.

        Raises:
            AttributeError: If there is no data to send.

        Returns:
            Coroutine: A coroutine that should be awaited, The return value of the coroutine would contain
             The response from the WhatsApp API.
        """

        if not data:
            raise AttributeError("No data to send")

        # Convert message_body to JSON
        json_data = json.dumps(data, cls=MyEncoder)

        timeout_secs = 10
        response = requests.post(
            self.WA_URL, headers=self.HEADERS, data=json_data, timeout=timeout_secs
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            # Re raise the error with the text gotten
            raise CustomHTTPError(
                status_code=response.status_code, response_text=response.text
            ) from exc

        return response.json()
