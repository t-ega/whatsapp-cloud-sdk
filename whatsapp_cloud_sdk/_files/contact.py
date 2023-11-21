"""This module contains an object that represents a Whatsapp Contact and it related details."""

from typing import List, Optional, Union

from whatsapp_cloud_sdk._files.file_object import File
from whatsapp_cloud_sdk._utils.types import JSONDict

from whatsapp_cloud_sdk._validators.messages import (
    AddressValidator,
    NameValidator,
    PhoneValidator,
    OrgValidator,
    URLValidator,
    EmailValidator,
)


# pylint: disable=redefined-builtin
# pylint: disable=too-few-public-methods
class Address(File):
    """
    Represents a contact address.

    Args:
        street (str): The street address.
        city (str): The city.
        state (str): The state.
        zip (str): The ZIP code.
        country (str): The country.
        country_code (str): The country code.
        type (str): The type of address.

    Attributes:
        street (str): The street address.
        city (str): The city.
        state (str): The state.
        zip (str): The ZIP code.
        country (str): The country.
        country_code (str): The country code.
        type (str): The type of address.
    """

    __slots__ = (
        "street",
        "city",
        "state",
        "zip",
        "country",
        "country_code",
        "type",
    )

    # pylint: disable=too-many-arguments
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip: str,
        country: str,
        country_code: str,
        type: str,
    ):
        validator = AddressValidator(
            street=street,
            city=city,
            state=state,
            zip=zip,
            country=country,
            country_code=country_code,
            type=type,
        )
        self.street = validator.street
        self.city = validator.city
        self.state = validator.state
        self.zip = validator.zip
        self.country = validator.country
        self.country_code = validator.country_code
        self.type = validator.type


class Email(File):
    """
    Represents an email address.

    Args:
        email (str): The email address.
        type (str): The type of email address.

    Attributes:
        email (str): The email address.
        type (str): The type of email address.
    """

    __slots__ = ("email", "type")

    def __init__(self, email: str, type: str):
        validator = EmailValidator(email=email, type=type)
        self.email = validator.email
        self.type = validator.type


class Name(File):
    """
    Represents a contact name.

    Args:
        formatted_name (str): The formatted name.
        first_name (str): The first name.
        last_name (str): The last name (optional).
        middle_name (str): The middle name (optional).
        suffix (str): The name suffix (optional).
        prefix (str): The name prefix (optional).

    Attributes:
        formatted_name (str): The formatted name.
        first_name (str): The first name.
        last_name (str): The last name.
        middle_name (str): The middle name.
        suffix (str): The name suffix.
        prefix (str): The name prefix.
    """

    __slots__ = (
        "formatted_name",
        "first_name",
        "last_name",
        "middle_name",
        "suffix",
        "prefix",
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        formatted_name: str,
        first_name: str,
        last_name: str = None,
        middle_name: str = "",
        suffix: str = "",
        prefix: str = "",
    ):
        validator = NameValidator(
            formatted_name=formatted_name,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            suffix=suffix,
            prefix=prefix,
        )
        self.formatted_name = validator.formatted_name
        self.first_name = validator.first_name
        self.last_name = validator.last_name
        self.middle_name = validator.middle_name
        self.suffix = validator.suffix
        self.prefix = validator.prefix


class Org(File):
    """
    Represents organizational information.

    Args:
        company (str): The company name.
        department (str): The department.
        title (str): The job title.

    Attributes:
        company (str): The company name.
        department (str): The department.
        title (str): The job title.
    """

    __slots__ = ("company", "department", "title")

    def __init__(self, company: str, department: str, title: str):
        validator = OrgValidator(company=company, department=department, title=title)
        self.company = validator.company
        self.department = validator.department
        self.title = validator.title


class Phone(File):
    """
    Represents a Whatsapp message phone number.

    Args:
        phone (str): The phone number.
        wa_id (str): The WhatsApp ID (optional).
        type (str): The type of phone number (optional).

    Attributes:
        phone (str): The phone number.
        wa_id (str): The WhatsApp ID.
        type (str): The type of phone number.
    """

    __slots__ = ("phone", "wa_id", "type")

    def __init__(self, phone: str, wa_id: str = None, type: str = None):
        validator = PhoneValidator(phone=phone, wa_id=wa_id, type=type)
        self.phone = validator.phone
        self.wa_id = validator.wa_id
        self.type = validator.type


class URL(File):
    """
    Represents a Whatsapp Message URL.

    Args:
        url (str): The URL.
        type (str): The type of URL.

    Attributes:
        url (str): The URL.
        type (str): The type of URL.
    """

    __slots__ = ("url", "type")

    def __init__(self, url: str, type: str):
        validator = URLValidator(url=url, type=type)
        self.url = validator.url
        self.type = validator.type


class Contact(File):
    """
    Represents a contact.

    Args:
        name [Name]: The contact's name. This is a required field.
        addresses Optional[List[Address]]: A list of addresses.
        birthday Optional[str]: The contact's birthday.
        emails Optional[List[Email]]: A list of email addresses.
        org Optional[Org]: Organizational information.
        phones Optional[List[Phone]]: A list of phone numbers.
        urls Optional[List[URL]]: A list of URLs.

    Attributes:
        name Optional[Name]: The contact's name This field is required.
        addresses Optional[List[Address]]: A list of addresses.
        birthday (Optional[str]): The contact's birthday.
        emails (Optional[List[Email]]): A list of email addresses.
        org (Optional[Org]): Organizational information.
        phones (Optional[List[Phone]]): A list of phone numbers.
        urls (Optional[List[URL]]): A list of URLs.

    Methods:
        - de_json(data: Optional[JSONDict]) -> Optional[Contact]: Create a Contact
        object from JSON data.
    """

    _id_attrs = ("name", "phones", "birthday")

    __slots__ = (
        "name",
        "addresses",
        "birthday",
        "emails",
        "org",
        "phones",
        "urls",
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: Union[Name, str],
        addresses: Optional[List[Address]] = None,
        birthday: Optional[str] = None,
        emails: Optional[List[Email]] = None,
        org: Optional[Org] = None,
        phones: Optional[Union[List[Phone], List[str]]] = None,
        urls: Optional[List[URL]] = None,
    ):
        # pylint: disable=fixme
        # TODO: Allow validation using pydantic

        #  required
        if isinstance(name, str):
            self.name = Name(formatted_name=name, first_name=name)
        elif isinstance(name, Name):
            self.name = name
        else:
            raise TypeError(
                "Name must either be a string or an instance of the Name class!"
            )

        if isinstance(phones, list):
            for i, phone in enumerate(phones):
                if isinstance(phone, str):
                    phones[i] = Phone(phone=phone)
                elif not isinstance(phone, Phone):
                    raise TypeError(
                        f"Phone {i} must either be a string or an instance of the Phone class!"
                    )
        else:
            # pylint: disable=line-too-long
            raise ValueError(
                f"Phones must be of type <class list> of phones class or strings!\nGot {type(phones)} instead "
            )

        #  optional
        self.addresses = addresses
        self.birthday = birthday
        self.emails = emails
        self.org = org
        self.phones = phones
        self.urls = urls

    # pylint: disable=too-many-locals
    @classmethod
    def de_json(cls, data: Optional[JSONDict]) -> Optional["Contact"]:
        """This class acts as a method for extracting and converting JSON data gotten from
        Whatsapp Cloud API and converting them into internal objects that can be interacted with
        """

        data = cls.parse_data(data)

        if not data:
            return None

        addresses = []
        if "addresses" in data:
            for address_data in data["addresses"]:
                address = Address(**address_data)
                addresses.append(address)

        emails = []
        if "emails" in data:
            for email_data in data["emails"]:
                email = Email(**email_data)
                emails.append(email)

        name = None
        if "name" in data:
            name_data = data["name"]
            name = Name(**name_data)

        org = None
        if "org" in data:
            org_data = data["org"]
            org = Org(**org_data)

        phones = []
        if "phones" in data:
            for phone_data in data["phones"]:
                phone = Phone(**phone_data)
                phones.append(phone)

        urls = []
        if "urls" in data:
            for url_data in data["urls"]:
                url = URL(**url_data)
                urls.append(url)

        return cls(
            name=name,
            addresses=addresses,
            birthday=data.get("birthday"),
            emails=emails,
            org=org,
            phones=phones,
            urls=urls,
        )


# pylint: enable=too-many-arguments
