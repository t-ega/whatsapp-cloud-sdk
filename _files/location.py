from _files.file_object import File

"""This module contains an object that represents a Whatsapp Location"""


class Location(File):
    """
    Represents a Location object

    """

    __slots__ = ("latitude", "longitude", "name", "address")

    def __init__(self, latitude: str, longitude: str, name: str, address: str):
        """

        :param latitude: the latitude of the location
        :param longitude: the longitude of the location
        :param name: the name of the location
        :param address: the address of the location
        """
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.address = address
