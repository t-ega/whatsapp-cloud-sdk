from .file_object import File

"""This module contains an object that represents a Whatsapp Image"""


class Image(File):
    """This object represents a Whatsapp Image"""

    __slots__ = (
        "caption",
        "mime_type",
        "id",
        "sha256",
    )

    def __init__(self, caption: str, mime_type: str, sha256: str, _id: str):
        """

        :param caption: the caption for the image
        :param mime_type(optional):the specific image format or file extension. Here are some common MIME types for
         popular image formats:
            JPEG image: image/jpeg
            PNG image: image/png
            GIF image: image/gif
            BMP image: image/bmp
            TIFF image: image/tiff
            SVG image: image/svg+xml
        :param sha256: the image hash(optional)
        :param _id(optional):If this is a reply to an image.
        """
        self.caption = caption
        self.id = _id
        self.mime_type = mime_type
        self.sha256 = sha256
