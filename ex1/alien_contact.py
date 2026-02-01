"""Exercise 1: Alien Contact Logs."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ValidationError
from sys import stderr
from datetime import datetime


class ContactType(Enum):
    """Enum for different contact types."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Data class for an alie contact with automatic validation."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":
        """Validate input dynamically."""
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type is ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self

    def __str__(self) -> str:
        """Create a string representation of this alien contact."""
        return f"""\
ID: {self.contact_id}
Type: {self.contact_type.value}
Location: {self.location}
Signal: {self.signal_strength}/10
Duration: {self.duration_minutes} minutes
Witnesses: {self.witness_count}
Message: '{self.message_received}'"""


def create_alien_contact(**kwargs) -> None:
    """Create and print a new alien contact."""
    print("========================================")
    try:
        contact: AlienContact = AlienContact(**kwargs)
        print("Valid contact report:")
        print(contact)
    except ValidationError as error:
        print("Expected validation error:", file=stderr)
        print(error, file=stderr)


def main() -> None:
    """Define main entry of the program."""
    print("Alien Contact Log Validation")
    create_alien_contact(
        contact_id="AC_2024_001",
        timestamp="2026-01-27T12:09",
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print()
    create_alien_contact(
        contact_id="AC_2024_001",
        timestamp="2026-01-27T12:09",
        location="Area 51, Nevada",
        contact_type=ContactType.TELEPATHIC,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=1,
        message_received="Greetings from Zeta Reticuli",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("[Error]:", error, file=stderr)
