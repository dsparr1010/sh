from enum import Enum
import pytest
from rates.utils import get_format_with_datetime


class TestDatetime:

    pass

    # @pytest.mark.parametrize(
    #     "iso_format", ("2015-07-01T07:00:00-05:00", "2015-07-04T15:00:00+00:00")
    # )
    # def test_get_format_with_datetime(self, iso_format):
    #     iso = get_format_with_datetime(iso_format)
    # print(iso.timetuple())
    # print(iso.timetz())
    # print(iso.tzinfo) -> UTC
    # print(iso.astimezone().ctime())
    # print(iso.__dir__())
