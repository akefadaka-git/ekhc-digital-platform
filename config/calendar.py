"""Calendar-neutral date contracts with an Ethiopian-calendar adapter boundary."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Protocol


class CalendarPreference(StrEnum):
    ETHIOPIAN = "ethiopian"
    GREGORIAN = "gregorian"


@dataclass(frozen=True, slots=True)
class EthiopianDate:
    """Validated Ethiopian calendar date; conversion is delegated to an adapter."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if isinstance(self.year, bool) or not isinstance(self.year, int) or self.year < 1:
            raise ValueError("year must be a positive integer.")
        if (
            isinstance(self.month, bool)
            or not isinstance(self.month, int)
            or not 1 <= self.month <= 13
        ):
            raise ValueError("month must be between 1 and 13.")
        if isinstance(self.day, bool) or not isinstance(self.day, int) or self.day < 1:
            raise ValueError("day must be positive.")
        final_month_days = 6 if (self.year + 1) % 4 == 0 else 5
        maximum = final_month_days if self.month == 13 else 30
        if self.day > maximum:
            raise ValueError("day is outside the selected Ethiopian month.")


class EthiopianCalendarAdapter(Protocol):
    """Conversion boundary implemented only by a verified calendar provider."""

    def from_gregorian(self, value: date) -> EthiopianDate: ...

    def to_gregorian(self, value: EthiopianDate) -> date: ...


def resolve_calendar_date(
    value: date,
    preference: CalendarPreference,
    adapter: EthiopianCalendarAdapter,
) -> date | EthiopianDate:
    """Return the date in the explicitly selected calendar, without guessing."""
    if not isinstance(value, date):
        raise TypeError("value must be a date.")
    if preference is CalendarPreference.GREGORIAN:
        return value
    if preference is CalendarPreference.ETHIOPIAN:
        return adapter.from_gregorian(value)
    raise ValueError("unsupported calendar preference.")
