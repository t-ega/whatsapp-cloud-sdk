from _files.file_object import File

"""This module contains an object that represents a Whatsapp Sticker"""


class Sticker(File):
    __slots__ = ("mime_type", "sha256", "id")

    def __init__(self, mime_type: str, sha256: str, id: str):
        self.id = id
        self.sha256 = sha256
        self.mime_type = mime_type
