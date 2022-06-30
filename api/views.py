import base64
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from movies.models import Movie
from reservation.models import PlayingTime
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeSerializer
from rest_framework import viewsets
# Create your views here.


class ObtainAuthTokenBase64(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": base64.b64encode(token.key.encode("ascii"))})


get_token_base64 = ObtainAuthTokenBase64.as_view()


class MoviesPlayingThisWeekViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ModelViewSet):
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeSerializer