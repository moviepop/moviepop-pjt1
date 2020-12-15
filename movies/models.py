from django.db import models


# Create your models here.
# from django.contrib.auth import get
class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# class Actor(models.Model):
#     name = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name


# class Country(models.Model):
#     iso = models.CharField(max_length=10, primary_key=True)
#     name = models.CharField(max_length=20)

#     def __str__(self):
#         return  self.name


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=200, null=True)
    backdrop_path = models.CharField(max_length=200, null=True)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    vote_average = models.FloatField()
    overview = models.TextField(null=True)
    release_date = models.DateField(auto_now=False)
    genres = models.ManyToManyField(Genre, related_name='movies')
    # runtime = models.IntegerField(null=True)
    # country = models.ManyToManyField(Country, related_name='movies')
    # actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title