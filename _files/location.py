from _files.file_object import File

"""This module contains an object that represents a Whatsapp Location"""


class Location(File):
    __slots__ = ("latitude", "longitude", "name", "address")

    def __init__(self, latitude: str, longitude: str, name: str, address: str):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.address = address
