"""This module contains an object that represents a Whatsapp Sticker"""


from whatsapp_cloud_sdk._files.file_object import File


# pylint: disable=too-few-public-methods
class Sticker(File):
    """Represents a WhatsApp sticker."""

    __slots__ = ("mime_type", "sha256", "id")

    # pylint: disable=redefined-builtin
    def __init__(self, mime_type: str, sha256: str, id: str):
        """
        Initialize a Sticker instance.

        Args:
            mime_type (str): The MIME type of the sticker.
            sha256 (str): The SHA256 hash of the sticker.
            id (str): The unique ID associated with the sticker.
        """
        self.id = id
        self.sha256 = sha256
        self.mime_type = mime_type
