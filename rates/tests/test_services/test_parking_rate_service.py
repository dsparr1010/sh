import pytest
from datetime import datetime
from rates.exceptions import NothingToUpdate
from rates.services.parking_rate_service import ParkingRateService


class TestParkingRateService:

    @pytest.mark.parametrize(
        "dt,expectation",
        (
            ("2022-05-01T12:30:45-05:00", "2022-05-01 17:30:45+0000"),  # EST -> UTC
            (
                "2015-07-04T15:00:00+00:00",
                "2015-07-04 15:00:00+0000",
            ),  # UTC remains UTC
            (
                "2023-07-15T14:30:00+01:00",
                "2023-07-15 13:30:00+0000",
            ),  # BST (British Summer Time) -> UTC
            (
                "2024-09-30T18:45:00+09:00",
                "2024-09-30 09:45:00+0000",
            ),  # JST (Japan Standard Time) -> UTC
        ),
    )
    def test_convert_timezone_to_utc(self, dt, expectation):
        """Test that datetime objects from non-UTC timezones convert to expected UTC value"""
        dt_iso_format = datetime.fromisoformat(dt)
        expected_dt = datetime.fromisoformat(expectation)

        converted_dt = ParkingRateService.convert_timezone(
            datetime_obj=dt_iso_format, timezone="UTC"
        )

        assert converted_dt == expected_dt

    @pytest.mark.parametrize(
        "time,timezone,expectation",
        (
            ("0900", "America/Chicago", "14:00:00"),  # 9am CST -> 2pm UTC
            ("1430", "Europe/London", "13:30:00"),  # 2:30pm BST -> 1:30 UTC
            ("1845", "Asia/Tokyo", "09:45:00"),  # 6:45pm JST -> 9:45am UTC
        ),
    )
    def test_convert_plain_text_time_tz_to_utc(self, time, timezone, expectation):
        """Test that a given time and a non-UTC timezone convert to expected UTC value"""
        converted_dt = ParkingRateService().convert_plain_text_time_tz_to_utc(
            time=time, tz=timezone
        )
        assert converted_dt == expectation

    @pytest.mark.django_db(transaction=True)
    def test_update_rate_instance_updates_price(
        self, all_parking_rates, parking_rate_fri_sat_sun
    ):
        """Test that a price is updated"""
        original_price = parking_rate_fri_sat_sun.price
        data = {
            "days": "fri,sat,sun",
            "start_time_utc": "14:00:00",
            "end_time_utc": "02:00:00",
            "price": 2500,
        }
        result = ParkingRateService.update_rate_instance(**data)
        assert result.price != original_price
        assert result.price == data["price"]

    @pytest.mark.django_db(transaction=True)
    def test_update_rate_instance_does_not_update_if_price_is_unchanged(
        self, parking_rate_fri_sat_sun
    ):
        """Test that an instance is not updated when existing instance is identical"""
        data = {
            "days": "fri,sat,sun",
            "start_time_utc": "14:00:00",
            "end_time_utc": "02:00:00",
            "price": 2000,
        }
        with pytest.raises(NothingToUpdate):
            ParkingRateService.update_rate_instance(**data)
