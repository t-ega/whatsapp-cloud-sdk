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
        return await self.get_bot().send_text(
            text=text, message_id=self.id, recipient_number=self.from_user
        )

    def get_bot(self) -> Optional[Bot]:
        if not self.__bot:
            raise RuntimeError("Bot is not available")
        return self.__bot

    async def reply_with_image_link(
        self, link: str, caption: Optional[str] = None
    ) -> Coroutine:
        return await self.get_bot().send_image_by_url(
            link=link,
            recipient_number=self.from_user,
            message_id=self.id,
            caption=caption,
        )

    async def reply_with_audio_link(self, link: str) -> Coroutine:
        return await self.get_bot().send_audio_by_url(
            link=link,
            recipient_number=self.from_user,
            message_id=self.id,
        )

    async def reply_with_document_link(
        self, link: str, caption: Optional[str]
    ) -> Coroutine:
        return await self.get_bot().send_document_by_url(
            link=link,
            caption=caption,
            recipient_number=self.from_user,
            message_id=self.id,
        )

    async def reply_with_sticker_link(self, link: str) -> Coroutine:
        return await self.get_bot().send_sticker_with_url(
            link=link, recipient_number=self.from_user, message_id=self.id
        )

    async def reply_with_video_link(
        self, link: str, caption: Optional[str] = None
    ) -> Coroutine:
        return await self.get_bot().send_video_by_url(
            link=link,
            recipient_number=self.from_user,
            caption=caption,
            message_id=self.id,
        )

    async def mark_message_as_read(
        self,
    ) -> Coroutine:
        return await self.get_bot().mark_message_as_read(message_id=self.id)

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: Bot) -> Optional["Message"]:
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
        attributes = {}
        for attr in self._id_attrs:
            attributes[attr] = getattr(self, attr)
        return str(attributes)
