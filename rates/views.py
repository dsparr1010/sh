from django.shortcuts import render
from rates.exceptions import UnavailableTimeSpansError
from rates.serializers import PriceQueryParamsDeserializer
from rest_framework import generics
from rest_framework.response import Response


class PriceListView(generics.ListAPIView):

    # will probably have to update this to the SERIALIZER instead of the DESERIALIZER
    serializer_class = PriceQueryParamsDeserializer

    def get_queryset(self):
        serializer = PriceQueryParamsDeserializer(data=self.request.query_params)
        try:
            if serializer.is_valid(raise_exception=True):
                start_time = self.request.query_params["start"]
                end_time = self.request.query_params["end"]

                # TODO: create model; then we can query between the times

        except UnavailableTimeSpansError as err:
            Response(
                {"message": str(err.message)},
                status=err.status_code,
            )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class

        return Response(
            data={
                "days": "mon,tues,thurs",
                "times": "0900-2100",
                "tz": "America/Chicago",
                "price": 1500,
            },
        )
