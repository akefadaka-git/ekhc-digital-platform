"""Ethiopian Amete Mihret calendar adapter based on ICU CECalendar arithmetic.

The conversion uses the published ICU/CECalendar Julian-day epoch and four-year
cycle rules. It is intentionally limited to positive Amete Mihret years.
"""

from datetime import date

from config.calendar import EthiopianDate

_JD_EPOCH_OFFSET_AMETE_MIHRET = 1_723_856
_GREGORIAN_ORDINAL_TO_JD = 1_721_425
_DAYS_PER_FOUR_YEAR_CYCLE = 1_461


class IcuEthiopianCalendarAdapter:
    """Pure-Python adapter implementing the ICU Ethiopic calendar arithmetic."""

    def to_gregorian(self, value: EthiopianDate) -> date:
        if not isinstance(value, EthiopianDate):
            raise TypeError("value must be an EthiopianDate.")
        julian_day = (
            _JD_EPOCH_OFFSET_AMETE_MIHRET
            + 365 * value.year
            + value.year // 4
            + 30 * (value.month - 1)
            + value.day
            - 1
        )
        return date.fromordinal(julian_day - _GREGORIAN_ORDINAL_TO_JD)

    def from_gregorian(self, value: date) -> EthiopianDate:
        if not isinstance(value, date):
            raise TypeError("value must be a date.")
        julian_day = value.toordinal() + _GREGORIAN_ORDINAL_TO_JD
        days_since_epoch = julian_day - _JD_EPOCH_OFFSET_AMETE_MIHRET
        if days_since_epoch < 0:
            raise ValueError("Gregorian date predates the Amete Mihret epoch.")

        cycle, remainder = divmod(days_since_epoch, _DAYS_PER_FOUR_YEAR_CYCLE)
        year = 4 * cycle + remainder // 365 - remainder // 1460
        day_of_year = 365 if remainder == 1460 else remainder % 365
        month = day_of_year // 30 + 1
        day = day_of_year % 30 + 1
        return EthiopianDate(year, month, day)
