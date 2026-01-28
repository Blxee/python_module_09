"""Exercise 0: Space Station Data."""

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional
from sys import stderr


class SpaceStation(BaseModel):
    """Space station dataclass with automatic field validation."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)

    def __str__(self) -> str:
        """Create a string representation of this SpaceStation."""
        return f"""\
ID: {self.station_id}
Name: {self.name}
Crew: {self.crew_size} people
Power: {self.power_level}%
Oxygen: {self.oxygen_level}%
Status: {"Operational" if self.is_operational else "Out of order"}"""


def create_space_station(**kwargs) -> None:
    """Create and print a new space station."""
    print("========================================")
    try:
        station: SpaceStation = SpaceStation(**kwargs)
        print("Valid station created:")
        print(station)
    except ValidationError as error:
        print("Expected validation error:", file=stderr)
        print(error, file=stderr)


def main() -> None:
    """Entry of the program."""
    print("Space Station Data Validation")

    # test with valid data
    create_space_station(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-01-27T12:09",
    )
    # test with crew_size out of range
    create_space_station(
        station_id="ISS001",
        name="International Space Station",
        crew_size=32,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-01-27T12:09",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("[Error]:", error, file=stderr)
