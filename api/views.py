import base64
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from cinemas.models import Hall
from movies.models import Movie
from reservation.models import PlayingTime, Reservation
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeSerializer, \
    PlayingTimeWithDetailsSerializer, ReservationSerializer, HallSerializer, UserReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PlayingTimeFilter
from rest_framework import viewsets, response, status
from rest_framework.permissions import IsAdminUser
# Create your views here.


class ObtainAuthTokenBase64(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": base64.b64encode(token.key.encode("ascii"))})


get_token_base64 = ObtainAuthTokenBase64.as_view()


class MoviesPlayingThisWeekViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeWithDetailsSerializer



class PlayingTimeViewSet(viewsets.ModelViewSet):
    queryset = PlayingTime.objects.order_by('start_time')
    serializer_class = PlayingTimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlayingTimeFilter


class MoviesAPIView(viewsets.ModelViewSet):
    queryset = Movie.objects.order_by('id')
    serializer_class = MovieSerializer


class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.order_by('id')
    serializer_class = HallSerializer


class UserReservationViewSet(viewsets.ModelViewSet):
    serializer_class = UserReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)



