from .FileObject import File

"""This module contains an object that represents a Whatsapp Image"""


class Image(File):
    __slots__ = (
        "caption",
        "mime_type",
        "id",
        "sha256",
    )

    def __init__(self, caption: str, mime_type: str, sha256: str, _id: str):
        self.caption = caption
        self.id = _id
        self.mime_type = mime_type
        self.sha256 = sha256
