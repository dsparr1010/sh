import json
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rates.exceptions import UnavailableTimeSpansError
from rates.models import ParkingRate
from rates.serializers import PriceQueryParamsDeserializer, PriceSerializer
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import replace_space_w_plus
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import JSONRenderer
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

                results = ParkingRateService.get_rates_within_datetimes(
                    start=start_time, end=end_time
                )

                queryset = QuerySet(model=ParkingRate, query=[])
                queryset._result_cache = results
                return queryset

            # elif serializer.errors:
            #     return ParkingRate.objects.none()
        except UnavailableTimeSpansError as err:
            return ParkingRate.objects.none()

    @action(methods=["GET"], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if len(queryset) == 0:
            # No applicable instances found - returning "unavailable"
            return Response(
                "unavailable",
                status=status.HTTP_200_OK,
            )
        return Response(serializer.data)
