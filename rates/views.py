from django.db.models import QuerySet
from rates.exceptions import UnavailableTimeSpansError
from rates.models import ParkingRate
from rates.serializers import PriceQueryParamsDeserializer, PriceSerializer
from rates.services.parking_rate_service import ParkingRateService
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response


class PriceListView(viewsets.GenericViewSet, ListModelMixin):

    serializer_class = PriceSerializer

    def _contains_space(self, s):
        return any(c.isspace() for c in s)

    def get_queryset(self):
        qps = self.request.query_params.copy()
        start_time = qps.get("start")
        end_time = qps.get("end")

        start_contains_space = self._contains_space(start_time)
        end_contains_space = self._contains_space(end_time)
        if start_contains_space:
            qps["start"] = start_time.replace(" ", "+")
        if end_contains_space:
            qps["end"] = end_time.replace(" ", "+")

        serializer = PriceQueryParamsDeserializer(data=qps)

        try:
            if serializer.is_valid(raise_exception=True):
                start_time = self.request.query_params["start"]
                end_time = self.request.query_params["end"]

                # return ParkingRate.objects.all()

                # TODO: create model; then we can query between the times
                results = ParkingRateService().get_rates_within_datetimes(
                    start=start_time, end=end_time
                )
                queryset = QuerySet(model=ParkingRate, query=[])
                queryset._result_cache = results
                return queryset

        except UnavailableTimeSpansError as err:
            Response(
                {"message": str(err.message)},
                status=err.status_code,
            )

    @action(methods=["get"], detail=False)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
