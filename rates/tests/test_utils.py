import pytest
from datetime import datetime
from rates.utils import get_format_with_datetime, replace_space_w_plus


class TestUtils:

    pass

    @pytest.mark.parametrize(
        "iso_format", ("2015-07-01T07:00:00 05:00", "2015-07-04T15:00:00+00:00")
    )
    def test_get_format_with_datetime(self, iso_format):
        iso_dt = get_format_with_datetime(iso_format)
        assert isinstance(iso_dt, datetime)

    @pytest.mark.parametrize(
        "missing_plus,expectation",
        (
            ("2015-07-01T07:00:00 05:00", "2015-07-01T07:00:00+05:00"),
            ("2015-07-04T15:00:00 00:00", "2015-07-04T15:00:00+00:00"),
        ),
    )
    def test_replace_space_w_plus(self, missing_plus, expectation):
        assert replace_space_w_plus(string_dt=missing_plus) == expectation
