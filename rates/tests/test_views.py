from urllib.parse import urlencode
from django.urls import reverse
from rest_framework.test import APIClient


# TODO: figure this out


class TestPriceListView:
    url = reverse("rates:price-list")
    client = APIClient()

    def test_returns_200_when_time_range_spans_over_a_day(self):
        query_params = {
            "start": "2015-07-04T20:00:00+00:00",
            "end": "2015-07-08T20:00:00+00:00",
        }
        url_w_params = f"{self.url}?{urlencode(query_params)}"

        response = self.client.get(url_w_params)

        print(f"RESPONSE: {response}")
