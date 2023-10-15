from enum import Enum
from typing import Dict, Any, Union

"""This module contains custom typing aliases for internal use within the library.

Warning:
    Contents of this module are intended to be used internally by the library and *not* by the
    user. Changes to this module are not considered breaking changes and may not be documented in
    the changelog.
"""

JSONDict = Dict[str, Any]
"""Dictionary containing response from Whatsapp or data to send to the API."""

JSONExtract = Union[JSONDict, None]
"""Type containing either a dictionary or none"""


class MessageTypes(Enum):
    """Base type for all the message types that we are accounting for from whatsapp api"""

    image = "image"
    audio = "audio"
    text = "text"
    reaction = "reaction"
    sticker = "sticker"
    location = "location"
    unknown = "unknown"
