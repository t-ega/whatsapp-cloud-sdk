"""This module contains custom formatting class and aliases for internal use within the library.

Warning:
    Contents of this module are intended to be used internally by the library and *not* by the
    user. Changes to this module are not considered breaking changes and may not be documented in
    the changelog.
"""

from typing import List, Optional

from unicodedata import decimal

from _utils.types import JSONDict
from _validators.messages import ButtonContents


class LinkTypes:
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"


class MessageFormatter:
    """
    Provides methods for formatting messages and data for interaction with the WhatsApp API.

    Methods:
        - format_text_message(body: str, to: str, preview_url: bool = False, message_id: str = None) -> JSONDict:
        - format_button_message(to: str, text: str, buttons: List[ButtonContents], message_id: Optional[str])
        -> JSONDict:
        - format_reply_with_reaction(to: str, emoji, message_id: Optional[str]) -> JSONDict:
        - format_link_message(to: str, link: str, m_type: LinkTypes, caption: str = "", message_id: str =None
        -> JSONDict:
        - format_send_document_by_url(to: str, document_link: str, caption: str, is_reply: bool = False,
         message_id: str = None) -> JSONDict:
        - format_location_message(to: str, latitude: decimal, longitude: int, name: str, address: str,
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

    @staticmethod
    def format_location_message(
        to: str,
        latitude: decimal,
        longitude: int,
        name: str,
        address: str,
        message_id: Optional[str],
    ) -> JSONDict:
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
        return {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
