"""Independent regression vectors for the ICU Ethiopic calendar adapter."""

from datetime import date

from django.test import SimpleTestCase

from config.calendar import CalendarPreference, EthiopianDate, resolve_calendar_date
from config.ethiopian_calendar import IcuEthiopianCalendarAdapter


class IcuEthiopianCalendarAdapterTests(SimpleTestCase):
    def setUp(self):
        self.adapter = IcuEthiopianCalendarAdapter()

    def test_ethiopian_new_year_reference_vectors(self):
        vectors = (
            (EthiopianDate(2012, 1, 1), date(2019, 9, 12)),
            (EthiopianDate(2015, 1, 1), date(2022, 9, 11)),
            (EthiopianDate(2016, 1, 1), date(2023, 9, 12)),
            (EthiopianDate(2017, 1, 1), date(2024, 9, 11)),
        )
        for ethiopian, gregorian in vectors:
            with self.subTest(ethiopian=ethiopian):
                self.assertEqual(self.adapter.to_gregorian(ethiopian), gregorian)
                self.assertEqual(self.adapter.from_gregorian(gregorian), ethiopian)

    def test_pagume_six_and_following_new_year_boundary(self):
        self.assertEqual(
            self.adapter.to_gregorian(EthiopianDate(2011, 13, 6)),
            date(2019, 9, 11),
        )
        self.assertEqual(
            self.adapter.from_gregorian(date(2019, 9, 11)),
            EthiopianDate(2011, 13, 6),
        )
        self.assertEqual(
            self.adapter.to_gregorian(EthiopianDate(2012, 1, 1)),
            date(2019, 9, 12),
        )

    def test_pagume_five_in_non_leap_year(self):
        self.assertEqual(
            self.adapter.to_gregorian(EthiopianDate(2012, 13, 5)),
            date(2020, 9, 10),
        )

    def test_round_trip_across_month_and_year_boundaries(self):
        for value in (
            EthiopianDate(2011, 13, 5),
            EthiopianDate(2011, 13, 6),
            EthiopianDate(2012, 1, 1),
            EthiopianDate(2015, 6, 30),
            EthiopianDate(2016, 13, 5),
            EthiopianDate(2017, 1, 1),
        ):
            with self.subTest(value=value):
                self.assertEqual(
                    self.adapter.from_gregorian(self.adapter.to_gregorian(value)),
                    value,
                )

    def test_rejects_pre_epoch_gregorian_date(self):
        with self.assertRaisesMessage(ValueError, "predates the Amete Mihret epoch"):
            self.adapter.from_gregorian(date(1, 1, 1))

    def test_calendar_preference_uses_production_adapter_boundary(self):
        self.assertEqual(
            resolve_calendar_date(
                date(2019, 9, 12), CalendarPreference.ETHIOPIAN, self.adapter
            ),
            EthiopianDate(2012, 1, 1),
        )
