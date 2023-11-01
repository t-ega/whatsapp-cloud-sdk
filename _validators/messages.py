"""
This file defines a set of Pydantic models used for representing different types of
 messages and message components.

- TextMessage: Represents a text message.
- ButtonContents: Represents the contents of a button.
- ButtonMessage: Represents a message with buttons.
- LinkMessage: Represents a message with a link.
- LocationMessage: Represents a location message.

These models are used for validating and working with data related to different types
 of messages in the application.

Note:
- Pydantic is used for data validation and serialization/deserialization.
- The models enforce constraints on the data structure, such as field types, lengths,
and optional fields.
- The use of UUID for default values ensures unique button IDs.

See Also:
- pydantic.BaseModel: The base class for Pydantic models, used for data validation and
serialization.
- Pydantic Configuration: The configuration for Pydantic models, such as additional
constraints and settings.
"""

from typing import Optional, List
import uuid

from pydantic import ConfigDict, constr, BaseModel


class TextMessage(BaseModel):
    """
    Represents a text message.

    Args:
        text (str): The text content of the message.
        message_id (str, optional): An optional message ID.
        recipient_number (str): The recipient's phone number.

    Attributes:
        model_config (ConfigDict): Pydantic configuration for this model.
    """

    model_config = ConfigDict(extra="forbid")
    text: str
    message_id: Optional[str]
    recipient_number: constr(max_length=20, min_length=8)


class ButtonContents(BaseModel):
    """
    Represents the contents of a button.

    Args:
        id (str, optional): An optional button ID. Defaults to a UUID.
        title (str): The title or label of the button.

    Attributes:
        None
    """

    id: Optional[str] = str(uuid.uuid4())
    title: constr(max_length=20, min_length=1)


class ButtonMessage(BaseModel):
    """
    Represents a message with buttons.

    Args:
        text (str): The text content of the message.
        recipient_number (str): The recipient's phone number.
        buttons (List[ButtonContents]): A list of button contents.

    Attributes:
        None
    """

    text: str
    recipient_number: constr(max_length=12, min_length=8)
    buttons: List[ButtonContents]


class LinkMessage(BaseModel):
    """
    Represents a message with a link.

    Args:
        link (str): The URL link.
        caption (str, optional): An optional caption for the link.
        message_id (str, optional): An optional message ID.

    Attributes:
        None
    """

    link: str
    caption: Optional[str] = None
    message_id: Optional[str] = None


class LocationMessage(BaseModel):
    """
    Represents a location message.

    Args:
        longitude (int): The longitude of the location.
        name (str): The name of the location.
        address (str): The address of the location.

    Attributes:
        None
    """

    longitude: int
    name: str
    address: str


class AddressValidator(BaseModel):
    """
    Validates address information.

    Args:
        street (str, optional): The street address.
        city (str, optional): The city.
        state (str, optional): The state or region.
        zip (str, optional): The postal code or ZIP code.
        country (str, optional): The country.
        country_code (str, optional): The country code.
        type (str, optional): The type of address.

    Attributes:
        None
    """

    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    type: Optional[str] = None


class EmailValidator(BaseModel):
    """
    Validates email information.

    Args:
        email (str, optional): The email address.
        type (str, optional): The type of email.

    Attributes:
        None
    """

    email: Optional[str] = None
    type: Optional[str] = None


class NameValidator(BaseModel):
    """
    Validates name information.

    Args:
        formatted_name (str): The formatted full name.
        first_name (str): The first name.
        last_name (str, optional): The last name.
        middle_name (str, optional): The middle name.
        suffix (str, optional): The name suffix.
        prefix (str, optional): The name prefix.

    Attributes:
        None
    """

    formatted_name: str
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    suffix: Optional[str] = None
    prefix: Optional[str] = None


class OrgValidator(BaseModel):
    """
    Validates organization information.

    Args:
        company (str, optional): The company name.
        department (str, optional): The department.
        title (str, optional): The job title.

    Attributes:
        None
    """

    company: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None


class PhoneValidator(BaseModel):
    """
    Validates phone information.

    Args:
        phone (str): The phone number.
        wa_id (str, optional): The WhatsApp ID.
        type (str, optional): The type of phone number.

    Attributes:
        None
    """

    phone: str
    wa_id: Optional[str] = None
    type: Optional[str] = None


class URLValidator(BaseModel):
    """
    Validates URL information.

    Args:
        url (str): The URL.
        type (str, optional): The type of URL.

    Attributes:
        None
    """

    url: str
    type: Optional[str] = None
