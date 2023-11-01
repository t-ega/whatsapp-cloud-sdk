import datetime
from typing import Optional, Coroutine, List

from _files.file_object import File
from _utils.types import JSONDict, JSONExtract, MessageTypes
from bot import Bot
from _files.image import Image
from _files.location import Location
from _files.reaction import Reaction
from _files.sticker import Sticker

"""This module contains an object that represents a Whatsapp Message"""


class Message(File):
    """Represents an actual message instance"""

    __slots__ = (
        "business_id",
        "display_phone_number",
        "phone_number_id",
        "from_user",
        "id",
        "time",
        "text",
        "type",
        "reaction",
        "image",
        "sticker",
        "location",
        "__bot",
    )

    _id_attrs = ("id", "from_user", "type", "time")

    def __init__(
        self,
        business_id: Optional[int] = None,
        display_phone_number: Optional[str] = None,
        phone_number_id: Optional[int] = None,
        from_user: Optional[str] = None,
        _id: Optional[str] = None,
        time: Optional[str] = None,
        text: Optional[str] = None,
        _type: Optional[MessageTypes] = None,
        reaction: Optional[Reaction] = None,
        image: Optional[Image] = None,
        sticker: Optional[Sticker] = None,
        location: Optional[Location] = None,
        bot: Bot = None,
    ):
        """
        Initialize a Message instance.

        Args:
            business_id (Optional[int]): The business ID associated with the message.
            display_phone_number (Optional[str]): The phone number to display.
            phone_number_id (Optional[int]): The ID of the phone number.
            from_user (Optional[str]): The sender of the message.
            _id (Optional[str]): The ID of the message.
            time (Optional[str]): The timestamp of the message.
            text (Optional[str]): The text of the message.
            _type (Optional[MessageTypes]): The type of the message.
            reaction (Optional[Reaction]): The reaction to the message.
            image (Optional[Image]): The image associated with the message.
            sticker (Optional[Sticker]): The sticker associated with the message.
            location (Optional[Location]): The location associated with the message.
            bot (Bot): The associated Bot instance.
        """
        # required
        self.id = _id
        # optional
        self.business_id = business_id
        self.display_phone_number = display_phone_number
        self.phone_number_id = phone_number_id
        self.from_user = from_user
        self.time = time
        self.text = text
        self.type: MessageTypes = _type
        self.reaction = reaction
        self.image = image
        self.sticker = sticker
        self.location = location
        self.__bot = bot

    async def reply_text(self, text: str) -> Coroutine:
        """
        Reply to the message with text.

        Args:
            text (str): The text to send in the reply.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_text(
            text=text, message_id=self.id, recipient_number=self.from_user
        )

    def get_bot(self) -> Optional[Bot]:
        """
        Get the associated Bot instance.

        Returns:
            Optional[Bot]: The associated Bot instance or None.
        """
        if not self.__bot:
            raise RuntimeError("Bot is not available")
        return self.__bot

    async def reply_with_image_link(
        self, link: str, caption: Optional[str] = None
    ) -> Coroutine:
        """
        Reply to the message with an image from a URL.

        Args:
            link (str): The URL of the image.
            caption (Optional[str]): The caption for the image.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_image_by_url(
            link=link,
            recipient_number=self.from_user,
            message_id=self.id,
            caption=caption,
        )

    async def reply_with_audio_link(self, link: str) -> Coroutine:
        """
        Reply to the message with audio from a URL.

        Args:
            link (str): The URL of the audio.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_audio_by_url(
            link=link,
            recipient_number=self.from_user,
            message_id=self.id,
        )

    async def reply_with_document_link(
        self, link: str, caption: Optional[str]
    ) -> Coroutine:
        """
        Reply to the message with a document from a URL.

        Args:
            link (str): The URL of the document.
            caption (Optional[str]): The caption for the document.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_document_by_url(
            link=link,
            caption=caption,
            recipient_number=self.from_user,
            message_id=self.id,
        )

    async def reply_with_sticker_link(self, link: str) -> Coroutine:
        """
        Reply to the message with a sticker from a URL.

        Args:
            link (str): The URL of the sticker.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_sticker_with_url(
            link=link, recipient_number=self.from_user, message_id=self.id
        )

    async def reply_with_video_link(
        self, link: str, caption: Optional[str] = None
    ) -> Coroutine:
        """
        Reply to the message with a video from a URL.

        Args:
            link (str): The URL of the video.
            caption (Optional[str]): The caption for the video.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().send_video_by_url(
            link=link,
            recipient_number=self.from_user,
            caption=caption,
            message_id=self.id,
        )

    async def mark_message_as_read(
        self,
    ) -> Coroutine:
        """
        Mark the message as read.

        Returns:
            Coroutine: A response coroutine from the WhatsApp Cloud API.
        """
        return await self.get_bot().mark_message_as_read(message_id=self.id)

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: Bot) -> Optional["Message"]:
        """
        Deserialize JSON data into a Message instance.

        Args:
            data (Optional[JSONDict]): The JSON data to deserialize.
            bot (Bot): The associated Bot instance.

        Returns:
            Optional[Message]: The deserialized Message instance or None.
        """
        data: JSONDict = data.copy().get("entry")[0]
        data: JSONDict = data.get("changes")[0]
        data: JSONDict = data.get("value")

        output_dict = {}

        if not data:
            return None

        messages: List = data.get("messages")

        if not messages:
            return None

        messages: JSONDict = messages[0]
        text: JSONExtract = messages.get("text")
        reaction: JSONExtract = messages.get("reaction")
        location: JSONExtract = messages.get("location")

        sticker: JSONExtract = messages.get("sticker")
        image: JSONExtract = messages.get("image")
        time = messages.get("timestamp")

        try:
            time = int(time)
            time = datetime.datetime.fromtimestamp(time)
        except ValueError:
            pass

        message_type = messages.get("type")

        if message_type and message_type in MessageTypes.__members__:
            output_dict["_type"] = MessageTypes[message_type]
        else:
            output_dict["_type"] = MessageTypes.unknown

        output_dict["business_id"] = output_dict.get("id")
        output_dict["display_phone_number"] = output_dict.get("display_phone_number")
        output_dict["phone_number_id"] = output_dict.get("phone_number_id")
        output_dict["from_user"] = messages.get("from")
        output_dict["_id"] = messages.get("id")
        output_dict["time"] = time
        output_dict["text"] = text and text.get("body") or None
        output_dict["reaction"] = reaction and Reaction(**reaction) or None
        output_dict["image"] = image and Image(**image) or None
        output_dict["sticker"] = sticker and Sticker(**sticker) or None
        output_dict["location"] = location and Location(**location) or None

        return cls(bot=bot, **output_dict)

    def __str__(self):
        """
        Convert the Message instance to a string representation.

        Returns:
            str
        """
        attributes = {}
        for attr in self._id_attrs:
            attributes[attr] = getattr(self, attr)
        return str(attributes)
