from _files.FileObject import File

"""This module contains an object that represents a Whatsapp Reaction"""


class Reaction(File):
    __slots__ = ("emoji", "reaction_id")

    def __init__(self, emoji, reaction_id: str):
        self.emoji = emoji
        self.reaction_id = reaction_id
