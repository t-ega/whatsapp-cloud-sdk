"""This module contains the base object that represents a Whatsapp File.
Other file objects would inherit from this."""

from typing import Optional
from warnings import warn

from whatsapp_tega._utils.types import JSONDict


class File:
    """Base Class for all file objects."""

    __slots__ = ()
    _id_attrs = ()

    def __str__(self):
        """Return a string representation of the object."""
        attributes = {}
        for slot in self.__slots__:
            attr = getattr(self, slot)
            if hasattr(attr, "to_dict"):
                attr = attr.to_dict()
            attributes[slot] = attr
        return str(attributes)

    def __eq__(self, other):
        """Check for equivalence with another object of the same class."""
        if isinstance(other, self.__class__):
            if not self._id_attrs:
                warn(
                    f"Objects of type {self.__class__.__name__} can not be meaningfully tested for"
                    " equivalence.",
                    stacklevel=2,
                )
            if not other._id_attrs:
                warn(
                    f"Objects of type {other.__class__.__name__} can not be meaningfully tested"
                    " for equivalence.",
                    stacklevel=2,
                )
            return self._id_attrs == other._id_attrs
        return super().__eq__(other)

    def to_dict(self) -> JSONDict:
        """Convert the object to a dictionary."""
        attributes = {}

        for slot in self.__slots__:
            attr = getattr(self, slot)

            if hasattr(attr, "to_dict"):
                attr = attr.to_dict()

            attributes[slot] = attr
        return attributes

    @staticmethod
    def parse_data(data: Optional[JSONDict]) -> Optional[JSONDict]:
        """Parse data and return as a dictionary."""
        return None if not data else data.copy()
