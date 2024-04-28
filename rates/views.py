from rates.exceptions import NoInstanceFound, NothingToUpdate, UnavailableTimeSpansError
from rates.models import ParkingRate
from rates.serializers import (
    PriceQueryParamsDeserializer,
    PriceSerializer,
    RateDeserializer,
    RateSerializer,
)
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import replace_space_w_plus
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response


class PriceListView(ListModelMixin, viewsets.GenericViewSet):

    serializer_class = PriceSerializer

    def get_queryset(self):
        qps = self.request.query_params.copy()
        start_time = qps.get("start")
        end_time = qps.get("end")

        qps["start"] = replace_space_w_plus(string_dt=start_time)
        qps["end"] = replace_space_w_plus(string_dt=end_time)

        serializer = PriceQueryParamsDeserializer(data=qps)
        try:

            if serializer.is_valid(raise_exception=True):
                start_time = self.request.query_params["start"]
                end_time = self.request.query_params["end"]

                return ParkingRateService.get_rates_within_datetimes(
                    start=start_time, end=end_time
                )

        except UnavailableTimeSpansError:
            return ParkingRate.objects.none()

    @action(methods=["GET"], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if len(queryset) == 0:
            # No applicable instances found - returning "unavailable"
            return Response(
                "unavailable",
                status=status.HTTP_200_OK,
            )

        # Grab only instance and serialize
        queryset = queryset.first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class RatesListView(viewsets.GenericViewSet, ListModelMixin):
    queryset = ParkingRate.objects.all()
    serializer_class = RateSerializer

    @action(methods=["GET"], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=False)
    def update(self, request, *args, **kwargs):
        deserializer = RateDeserializer(data=request.data)
        try:
            deserializer.is_valid()
            data = deserializer.data
            instance = ParkingRateService.update_rate_instance(**data)
            serializer = PriceSerializer(instance)
            return Response(serializer.data)
        except (NoInstanceFound, NothingToUpdate) as err:
            return Response(err.message, status=status.HTTP_200_OK)
