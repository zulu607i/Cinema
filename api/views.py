import base64
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from cinemas.models import Hall, Seat
from movies.models import Movie
from reservation.models import PlayingTime, Reservation
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeSerializer, \
    PlayingTimeWithDetailsSerializer, ReservationSerializer, HallSerializer, UserReservationSerializer, \
    ChangeReservationSeatStatusSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PlayingTimeFilter
from rest_framework import viewsets, response, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import Check_API_KEY_Auth
from rest_framework.decorators import api_view, permission_classes

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
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeWithDetailsSerializer



class PlayingTimeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PlayingTime.objects.order_by('start_time')
    serializer_class = PlayingTimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlayingTimeFilter


class MoviesAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.order_by('id')
    serializer_class = MovieSerializer


class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class HallViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Hall.objects.order_by('id')
    serializer_class = HallSerializer


class UserReservationViewSet(viewsets.ModelViewSet):
    serializer_class = UserReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


@permission_classes([Check_API_KEY_Auth])
@api_view(['GET'])
def change_seat_status(request, pk):
    seats = Seat.objects.get(pk=pk)
    serialseats = ChangeReservationSeatStatusSerializer(seats, many=False)
    if not seats.is_occupied:
        seats.is_occupied = True
    return Response(serialseats.data)