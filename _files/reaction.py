"""This module contains an object that represents a Whatsapp Reaction"""


from _files.file_object import File


# pylint: disable=too-few-public-methods
class Reaction(File):
    """Represents a WhatsApp reaction to a message."""

    __slots__ = ("emoji", "reaction_id")

    def __init__(self, emoji, reaction_id: str):
        """
        Initialize a Reaction instance.

        Args:
            emoji (str): The emoji representing the reaction.
            reaction_id (str): The unique ID associated with the reaction.
        """
        self.emoji = emoji
        self.reaction_id = reaction_id
