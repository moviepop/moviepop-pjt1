from rest_framework.serializers import ModelSerializer

from .models import Movie

class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'release_date', 'poster_path')