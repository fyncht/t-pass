from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Venue, Booking
from .serializers import TokenSerializer, VenueSerializer, BookingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from datetime import datetime

from rest_framework import generics, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'address']  # фильтр
    search_fields = ['name', 'description']  # поиск


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('venue')
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['venue', 'start_time', 'end_time']
    search_fields = ['venue__name']  # поиск по названию площадки

    @action(detail=False, methods=['post'])
    def cancel_all(self, request):
        Booking.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        venue_id = request.data.get('venue')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # get the  информацию о площадке
        try:
            venue = Venue.objects.get(id=venue_id)
        except venue.ObjectDoesNotExist:
            raise ValidationError('The venue is not found')

        # check, соответствует ли время бронирования графику работы площадки
        if not self.is_within_operating_hours(venue, start_time, end_time):
            raise ValidationError('The booking time is outside the venue\'s operating hours.')

        overlapping_bookings = Booking.objects.filter(
            venue_id=venue_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if overlapping_bookings.exists():
            raise ValidationError('This time slot is already booked.')

        return super().create(request, *args, **kwargs)

    def is_within_operating_hours(self, venue, start_time_str, end_time_str):
        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)

        # transforming время в строку формата часов для сравнения
        start_time_str = start_time.strftime('%H:%M')
        end_time_str = end_time.strftime('%H:%M')

        # get the расписание площадки для соответствующего дня
        day_of_week = start_time.strftime('%A').lower()
        operating_hours = venue.availability.get(day_of_week, '')

        if not operating_hours:
            return False  # net информации

        opening_time, closing_time = operating_hours.split('-')

        return opening_time <= start_time_str <= end_time_str <= closing_time

    def get_queryset(self):
        queryset = super().get_queryset()
        user_contact = self.request.query_params.get('user_contact')
        if user_contact:
            queryset = queryset.filter(user_contact=user_contact)
        past = self.request.query_params.get('past', None)
        if past is not None:
            if past.lower() == 'true':
                queryset = queryset.filter(end_time__lt=datetime.now())
            else:
                queryset = queryset.filter(end_time__gte=datetime.now())
        return queryset


# class LoginView(generics.CreateAPIView):
#     """
#     POST auth/login/
#     """
#     # This permission class will override the global permission
#     # class setting
#     permission_classes = (permissions.AllowAny,)
#
#     queryset = User.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             # login saves the user’s ID in the session,
#             # using Django’s session framework.
#             login(request, user)
#             serializer = TokenSerializer(data={
#                 # using drf jwt utility functions to generate a token
#                 "token": jwt_encode_handler(
#                     jwt_payload_handler(user)
#                 )})
#             serializer.is_valid()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
