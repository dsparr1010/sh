import pytest
from django.urls import reverse
from rates.exceptions import NoInstanceFound, NothingToUpdate
from rest_framework import status
from rest_framework.test import APIClient


class TestPriceListView:
    url = reverse("rates:price-list")
    client = APIClient()
    expected_error_msg = "unavailable"

    @pytest.mark.django_db(transaction=True)
    def test_returns_200_unavailable_when_time_range_spans_over_a_day(self):
        """Test view returns 'unavailable' when time spans over a day"""
        url_w_params = (
            f"{self.url}?start=2015-07-04T20:00:00-00:00&end=2015-07-08T20:00:00-00:00"
        )
        response = self.client.get(url_w_params)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.expected_error_msg

    @pytest.mark.parametrize(
        "start_time,end_time,parking_rate_fixture",
        (
            (
                "2015-07-01T06:00:00-05:00",  # Wednesday 6am CST
                "2015-07-01T17:00:00-05:00",  # -> 5pm CST
                "parking_rate_mon_wed_sat",
            ),
            (
                "2015-07-03T10:00:00-06:00",  # Friday 10am EST
                "2015-07-03T15:00:00-06:00",  # -> 4pm EST
                "parking_rate_fri_sat_sun",
            ),
            (
                "2015-07-02T23:00:00+09:00",  # Thursday 11pm JST
                "2015-07-02T23:05:00+09:00",  # -> 11:05pm JST
                "parking_rate_mon_tues_thurs",
            ),
            (
                "2015-07-01T07:00:00-05:00",  # Wednesday 1pm CST
                "2015-07-01T12:00:00-05:00",  # -> 5pm CST
                "parking_rate_mon_wed_sat",
            ),
        ),
    )
    @pytest.mark.django_db(transaction=True)
    def test_returns_200_when_applicable_time_span_found(
        self,
        start_time,
        end_time,
        parking_rate_fixture,
        all_parking_rates,
        request,
    ):
        """Test view returns correct rate"""
        matching_rate_fixture = request.getfixturevalue(parking_rate_fixture)
        url_w_params = f"{self.url}?start={start_time}&end={end_time}"
        response = self.client.get(url_w_params)
        assert "price" in response.data
        assert response.data["price"] == matching_rate_fixture.price

    @pytest.mark.django_db(transaction=True)
    def test_returns_unavailable_when_time_span_is_invalid(
        self, parking_rate_fri_sat_sun
    ):
        url_w_params = (
            f"{self.url}?start=2015-07-04T15:00:00+05:00&end=2015-07-04T20:00:00+00:00"
        )
        response = self.client.get(url_w_params)
        assert "unavailable" in response.data


class TestRatesListView:
    url = reverse("rates:rates-list")
    client = APIClient()

    # GET

    @pytest.mark.django_db(transaction=True)
    def test_get_returns_all_rates(self, all_parking_rates):
        """Test that a GET request returns all instances of ParkingRates"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(all_parking_rates)

    # PUT

    @pytest.mark.django_db(transaction=True)
    def test_put_updates_rate_instances_given_a_different_timezone(
        self, parking_rate_mon_wed_sat
    ):

        original_price = parking_rate_mon_wed_sat.price

        data = {
            "days": "mon,wed,sat",
            "times": "0200-0600",
            "tz": "America/New_York",
            "price": 2500,
        }

        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["price"] != original_price

    @pytest.mark.django_db(transaction=True)
    def test_put_does_not_update_if_instance_does_not_exist(
        self, parking_rate_mon_wed_sat
    ):
        """Test that an instance does not exist and is not updated"""
        data = {
            "days": "mon,wed,sat",
            "times": "0100-0500",
            "tz": "America/New_York",
            "price": 2500,
        }

        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == NoInstanceFound.message

    @pytest.mark.django_db(transaction=True)
    def test_put_does_not_update_if_no_data_discrepancy(self, parking_rate_mon_wed_sat):
        """Test that an instance equal to request data already exists and is not updated"""
        data = {
            "days": "mon,wed,sat",
            "times": "0100-0500",
            "tz": "America/Chicago",
            "price": 1000,
        }

        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == NothingToUpdate.message
