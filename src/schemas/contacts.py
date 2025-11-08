from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List


class CreateContactRequest(BaseModel):
    """
    Schema for creating a new contact.

    Attributes:
        name (str): The name of the contact.
        phone (str): The phone number of the contact in E.164 format.
    """
    name: str = Field(
        ..., 
        description="The name of the contact.",
        json_schema_extra={"example": "Amirul"}
    )
    phone: str = Field(
        ..., 
        description="Phone number in E.164 format.",
        json_schema_extra={"example": "+1234567890"}
    )


class Contact(BaseModel):
    """
    Schema for a contact resource.

    Attributes:
        id (str): Unique identifier for the contact.
        name (str): The name of the contact.
        phone (str): The phone number of the contact in E.164 format.
    """
    id: str = Field(..., description="Unique identifier for the contact.", json_schema_extra={"example": "contact123"})
    name: str = Field(..., description="The name of the contact.", json_schema_extra={"example": "Alice"})
    phone: str = Field(
        ..., 
        description="Phone number in E.164 format.", 
        json_schema_extra={"example": "+1234567890"}
    )


class ListContactsResponse(BaseModel):
    """
    Schema for listing contacts with pagination support.

    Attributes:
        contacts (List[Contact]): List of contact objects.
        page_number (int): Current page number.
        page_size (int): Number of contacts per page.
    """
    contacts: List[Contact] = Field(..., alias="contactsList", description="List of contact objects.")
    page_number: int = Field(..., alias="pageNumber", description="Current page number.", json_schema_extra={"example": 1})
    page_size: int = Field(..., alias="pageSize", description="Number of contacts per page.", json_schema_extra={"example": 10})

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
