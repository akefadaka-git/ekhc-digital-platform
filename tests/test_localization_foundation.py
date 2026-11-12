"""Tests for Unicode preservation and calendar adapter contracts."""

import unicodedata
from datetime import date

from django.test import SimpleTestCase

from config.calendar import (
    CalendarPreference,
    EthiopianDate,
    resolve_calendar_date,
)
from config.unicode import normalize_display_text


class UnicodeNormalizationTests(SimpleTestCase):
    def test_nfc_normalizes_combining_sequences_without_translation(self):
        source = "Cafe\u0301 አማርኛ"
        normalized = normalize_display_text(source)
        self.assertEqual(normalized, unicodedata.normalize("NFC", source))
        self.assertIn("አማርኛ", normalized)

    def test_normalization_preserves_whitespace_and_text(self):
        source = "  ቀጣና   ኅብረት  "
        self.assertEqual(normalize_display_text(source), source)

    def test_non_string_input_is_rejected(self):
        with self.assertRaisesMessage(TypeError, "value must be a string"):
            normalize_display_text(None)


class EthiopianDateValidationTests(SimpleTestCase):
    def test_regular_month_has_thirty_days(self):
        self.assertEqual(EthiopianDate(2016, 1, 30).day, 30)

    def test_pagume_has_five_days_in_non_leap_year(self):
        self.assertEqual(EthiopianDate(2016, 13, 5).day, 5)
        with self.assertRaisesMessage(ValueError, "outside the selected"):
            EthiopianDate(2016, 13, 6)

    def test_pagume_has_six_days_in_leap_year(self):
        self.assertEqual(EthiopianDate(2015, 13, 6).day, 6)

    def test_invalid_month_is_rejected(self):
        with self.assertRaisesMessage(ValueError, "month must be between"):
            EthiopianDate(2016, 14, 1)


class CalendarAdapterTests(SimpleTestCase):
    class FakeAdapter:
        def from_gregorian(self, value):
            return EthiopianDate(2016, 1, 1)

        def to_gregorian(self, value):
            return date(2023, 9, 12)

    def test_gregorian_preference_does_not_call_adapter(self):
        value = date(2023, 9, 12)
        self.assertEqual(
            resolve_calendar_date(value, CalendarPreference.GREGORIAN, object()),
            value,
        )

    def test_ethiopian_preference_uses_explicit_adapter(self):
        result = resolve_calendar_date(
            date(2023, 9, 12),
            CalendarPreference.ETHIOPIAN,
            self.FakeAdapter(),
        )
        self.assertEqual(result, EthiopianDate(2016, 1, 1))



class LanguageNegotiationTests(SimpleTestCase):
    def test_missing_preference_defaults_to_amharic(self):
        from config.localization import resolve_platform_language

        self.assertEqual(resolve_platform_language(""), "am")

    def test_explicit_english_preference_is_supported(self):
        from config.localization import resolve_platform_language

        self.assertEqual(resolve_platform_language("en-US,en;q=0.9,am;q=0.8"), "en")

    def test_highest_quality_supported_language_wins(self):
        from config.localization import resolve_platform_language

        self.assertEqual(resolve_platform_language("en;q=0.5,am;q=0.9"), "am")

    def test_unsupported_language_falls_back_to_amharic(self):
        from config.localization import resolve_platform_language

        self.assertEqual(resolve_platform_language("fr-CA,sw;q=0.8"), "am")
