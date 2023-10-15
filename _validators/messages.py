from pydantic import ConfigDict, constr, BaseModel
from typing import Optional, List
import uuid


"""
This file defines a set of Pydantic models used for representing different types of messages and message components.

- TextMessage: Represents a text message.
- ButtonContents: Represents the contents of a button.
- ButtonMessage: Represents a message with buttons.
- LinkMessage: Represents a message with a link.
- LocationMessage: Represents a location message.

These models are used for validating and working with data related to different types of messages in the application.

Note:
- Pydantic is used for data validation and serialization/deserialization.
- The models enforce constraints on the data structure, such as field types, lengths, and optional fields.
- The use of UUID for default values ensures unique button IDs.

See Also:
- pydantic.BaseModel: The base class for Pydantic models, used for data validation and serialization.
- Pydantic Configuration: The configuration for Pydantic models, such as additional constraints and settings.
"""


class TextMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    message_id: Optional[str]
    recipient_number: constr(max_length=20, min_length=8)


class ButtonContents(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: constr(max_length=20, min_length=1)


class ButtonMessage(BaseModel):
    text: str
    recipient_number: constr(max_length=12, min_length=8)
    buttons: List[ButtonContents]


class LinkMessage(BaseModel):
    link: str
    caption: Optional[str] = None
    message_id: Optional[str] = None


class LocationMessage(BaseModel):
    longitude: int
    name: str
    address: str


class AddressValidator(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    type: Optional[str] = None


class EmailValidator(BaseModel):
    email: Optional[str] = None
    type: Optional[str] = None


class NameValidator(BaseModel):
    formatted_name: str
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    suffix: Optional[str] = None
    prefix: Optional[str] = None


class OrgValidator(BaseModel):
    company: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None


class PhoneValidator(BaseModel):
    phone: str
    wa_id: Optional[str] = None
    type: Optional[str] = None


class URLValidator(BaseModel):
    url: str
    type: Optional[str] = None
