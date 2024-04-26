import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestPriceListView:
    url = reverse("rates:price-list")
    client = APIClient()
    expected_error_msg = "unavailable"

    @pytest.mark.django_db(transaction=True)
    def test_returns_200_unavailable_when_time_range_spans_over_a_day(self):
        url_w_params = (
            f"{self.url}?start=2015-07-04T20:00:00-00:00&end=2015-07-08T20:00:00-00:00"
        )
        response = self.client.get(url_w_params)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.expected_error_msg

    @pytest.mark.django_db(transaction=True)
    def test_returns_200_when_applicable_time_span_found(
        self, all_parking_rates, parking_rate_wed
    ):
        url_w_params = (
            f"{self.url}?start=2015-07-08T11:00:00-00:00&end=2015-07-08T15:00:00-00:00"
        )
        response = self.client.get(url_w_params)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0] == {"price": parking_rate_wed.price}
