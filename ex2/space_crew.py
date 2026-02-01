"""Exercise 2: Space Crew Management."""

from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from sys import stderr
from typing import Any


class Rank(Enum):
    """Define possible ranks of a crew member."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Data class for a crew member with validation."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True

    def __str__(self) -> str:
        """Create a string representation for this member."""
        return f"{self.name} ({self.rank.value}) - {self.specialization}"


class SpaceMission(BaseModel):
    """Data class for a space mission with validation."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        """Dynamically validate the data."""
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(
            member.rank in (Rank.CAPTAIN, Rank.COMMANDER)
            for member in self.crew
        ):
            raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            total_members: int = len(self.crew)
            experienced_members: int = len(
                [
                    member
                    for member in self.crew
                    if member.years_experience >= 5
                ]
            )
            if experienced_members / total_members < 0.5:
                raise ValueError(
                    "Long missions (> 365 days)"
                    " need 50% experienced crew (5+ years)"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self

    def __str__(self) -> str:
        """Create a string representation for this mission."""
        return f"""\
Mission: {self.mission_name}
ID: {self.mission_id}
Destination: {self.destination}
Duration: {self.duration_days} days
Budget: ${self.budget_millions}M
Crew size: {len(self.crew)}
Crew members:
{"\n".join("- " + str(member) for member in self.crew)}
"""


def create_space_mission(**kwargs) -> None:
    """Create and print a new space mission."""
    print("========================================")
    try:
        mission: SpaceMission = SpaceMission(**kwargs)
        print("Valid mission created:")
        print(mission)
    except ValidationError as error:
        print("Expected validation error:", file=stderr)
        print(error, file=stderr)


def main() -> None:
    """Define main entry of the program."""
    print("Space Mission Crew Validation")

    sarah: dict[str, Any] = {
        "member_id": "CREW_001",
        "name": "Sarah Connor",
        "rank": Rank.COMMANDER,
        "age": 32,
        "specialization": "Mission Command",
        "years_experience": 12,
    }
    john: dict[str, Any] = {
        "member_id": "CREW_002",
        "name": "John Smith",
        "rank": Rank.LIEUTENANT,
        "age": 26,
        "specialization": "Navigation",
        "years_experience": 3,
    }
    alice: dict[str, Any] = {
        "member_id": "CREW_003",
        "name": "Alice Johnson ",
        "rank": Rank.OFFICER,
        "age": 27,
        "specialization": "Engineering",
        "years_experience": 6,
    }

    crew: list[dict[str, Any]] = [sarah, john, alice]

    create_space_mission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2026-01-27T12:09",
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )

    sarah["rank"] = Rank.CADET

    create_space_mission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2026-01-27T12:09",
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("[Error]:", error, file=stderr)
