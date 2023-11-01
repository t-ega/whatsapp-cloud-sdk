from json import JSONEncoder

from _files.file_object import File


class MyEncoder(JSONEncoder):
    """Custom JSON encoder for serializing File objects e.g. Message, Audio, Video e.t.c.

    This encoder is used to customize the serialization behavior when converting objects to JSON format.

    Attributes:
        None

    Methods:
        default(o): Serialize an object to a JSON-serializable format.

    Args:
        o: The object to be serialized.

    Returns:
        JSON-serializable representation of the object.
    """

    def default(self, o):
        """Serialize an object to a JSON-serializable format.

        This method is called for objects that are not natively serializable by the JSON encoder.
        It checks if the object is an instance of the File class and calls it's to_dict() method for serialization.

        Args:
            o: The object to be serialized.

        Returns:
            JSON-serializable representation of the object.
        """
        if isinstance(o, File):
            return o.to_dict()

        return super().default(o)
