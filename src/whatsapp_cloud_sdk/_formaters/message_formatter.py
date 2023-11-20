"""This module contains custom formatting class and aliases for internal use within the library.

Warning:
    Contents of this module are intended to be used internally by the library and *not* by the
    user. Changes to this module are not considered breaking changes and may not be documented in
    the changelog.
"""
from enum import Enum
from typing import List, Optional

from unicodedata import decimal

from src.whatsapp_cloud_sdk._utils.types import JSONDict
from src.whatsapp_cloud_sdk._validators.messages import ButtonContents


class LinkTypes(Enum):
    """
    Constants representing different types of links.

    Attributes:
        AUDIO (str): A link type for audio content.
        IMAGE (str): A link type for image content.
        VIDEO (str): A link type for video content.
    """

    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"


class MessageFormatter:
    """
    Provides methods for formatting messages and data for interaction with the WhatsApp API.

    Methods:
        - format_text_message(body: str, to: str, preview_url: bool = False,
         message_id: str = None) -> JSONDict:
        - format_button_message(to: str, text: str, buttons: List[ButtonContents],
        message_id: Optional[str])
        -> JSONDict:
        - format_reply_with_reaction(to: str, emoji, message_id: Optional[str]) -> JSONDict:
        - format_link_message(to: str, link: str, m_type: LinkTypes, caption: str = "",
         message_id: str =None
        -> JSONDict:
        - format_send_document_by_url(to: str, document_link: str, caption: str,
        is_reply: bool = False,
         message_id: str = None) -> JSONDict:
        - format_location_message(to: str, latitude: decimal, longitude: int, name: str,
        address: str,
        message_id: Optional[str])
        -> JSONDict:
        - format_contact_message(contact: list, to: str, message_id: Optional[str]) -> JSONDict:
        - format_sticker_message_by_url(link: str, to: str, message_id: Optional[str]) -> JSONDict:
        - mark_message_as_read(message_id: str) -> JSONDict:
    """

    @staticmethod
    def format_text_message(
        body: str, to: str, preview_url: bool = False, message_id: str = None
    ) -> JSONDict:
        """
        Formats a text message for WhatsApp.

        Args:
        - body (str): The text message body.
        - to (str): The recipient's WhatsApp number.
        - preview_url (bool, optional): Whether to preview URLs in the message.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted text message.
        """

        body = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"preview_url": preview_url, "body": body},
        }

        if message_id:
            body["context"] = {"message_id": message_id}

        return body

    @staticmethod
    def format_button_message(
        to: str,
        text: str,
        buttons: List[ButtonContents],
        message_id: Optional[str],
    ) -> JSONDict:
        """
        Formats a message with interactive buttons for WhatsApp.

        Args:
        - to (str): The recipient's WhatsApp number.
        - text (str): The text message accompanying the buttons.
        - buttons (List[ButtonContents]): List of button contents.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted button message.

        """

        if not isinstance(buttons, ButtonContents):
            raise TypeError("Buttons must be an instance of button contents")

        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": buttons},
            },
        }

        if message_id:
            message["context"] = {"message_id": message_id}

        return message

    @staticmethod
    def format_reply_with_reaction(
        to: str,
        emoji,
        message_id: Optional[str],
    ) -> JSONDict:
        """
        Formats a message with interactive buttons for WhatsApp.

        Args:
        - to (str): The recipient's WhatsApp number.
        - text (str): The text message accompanying the buttons.
        - buttons (List[ButtonContents]): List of button contents.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted button message.
        """

        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "reaction",
            "reaction": {"message_id": message_id, "emoji": emoji},
        }

        if message_id:
            message["context"] = {"message_id": message_id}

        return message

    @staticmethod
    def format_link_message(
        to: str, link: str, m_type: LinkTypes, caption: str = "", message_id: str = None
    ) -> JSONDict:
        """
        Formats a reaction message with an emoji for WhatsApp.

        Args:
        - to (str): The recipient's WhatsApp number.
        - emoji: The emoji representing the reaction.
        - message_id (str, optional): The ID of the message being reacted to.

        Returns:
        - JSONDict: The formatted reaction message.
        """

        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": m_type,
            m_type: {"link": link},
        }

        if len(caption) > 0:
            message[m_type]["caption"] = caption

        if message_id:
            message["context"] = {"message_id": message_id}

        return message

    @staticmethod
    def format_send_document_by_url(
        to: str,
        document_link: str,
        caption: str,
        is_reply: bool = False,
        message_id: str = None,
    ) -> JSONDict:
        """
        Formats a document message with a link for WhatsApp.

        Args:
        - to (str): The recipient's WhatsApp number.
        - document_link (str): The URL of the document to send.
        - caption (str): The caption for the document.
        - is_reply (bool, optional): Indicates if it's a reply message.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted document message.
        """

        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "document",
            "document": {"link": document_link, "caption": caption},
        }

        if is_reply:
            if message_id is None:
                raise ValueError("message_id is required for a reply message.")
            message["context"] = {"message_id": message_id}

        return message

    # pylint: disable=too-many-arguments
    @staticmethod
    def format_location_message(
        to: str,
        latitude: decimal,
        longitude: int,
        name: str,
        address: str,
        message_id: Optional[str],
    ) -> JSONDict:
        """
        Formats a location message for WhatsApp.

        Args:
        - to (str): The recipient's WhatsApp number.
        - latitude (decimal): The latitude coordinate of the location.
        - longitude (int): The longitude coordinate of the location.
        - name (str): The name of the location.
        - address (str): The address of the location.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted location message.
        """
        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
                "address": address,
            },
        }

        if message_id:
            message["context"] = {"message_id": message_id}
        return message

    @staticmethod
    def format_contact_message(
        contacts: list,
        to: str,
        message_id: Optional[str],
    ) -> JSONDict:
        """
        Formats a contact message for WhatsApp.

        Args:
        - contacts (list): List of contact details (e.g., Name, Phone, Email).
        - to (str): The recipient's WhatsApp number.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted contact message.
        """
        message = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "contacts",
            "contacts": contacts,
        }

        if message_id:
            message["context"] = {"message_id": message_id}

        return message

    @staticmethod
    def format_sticker_message_by_url(
        link: str,
        to: str,
        message_id: Optional[str],
    ) -> JSONDict:
        """
        Formats a sticker message with a link for WhatsApp.

        Args:
        - link (str): The URL of the sticker image.
        - to (str): The recipient's WhatsApp number.
        - message_id (str, optional): The ID of the message being replied to.

        Returns:
        - JSONDict: The formatted sticker message.
        """
        message = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "sticker",
            "sticker": {"link": link},
        }

        if message_id:
            message["context"] = {"message_id": message_id}

        return message

    @staticmethod
    def mark_message_as_read(message_id: str):
        """
        Marks a message as read on WhatsApp.

        Args:
        - message_id (str): The ID of the message to mark as read.

        Returns:
        - JSONDict: The command to mark the message as read.
        """
        return {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
