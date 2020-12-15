from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name="index"),
    path('preference/', views.preference, name='preference'),
    path('released_thisyear/', views.released_thisyear, name="released_thisyear"),
    path('alone/', views.alone, name="alone"),
    path('couple/', views.couple, name="couple"),
    path('together/', views.together, name="together"),
    path('<title>/<int:date>/', views.naver_link, name='naver_link'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('search_title/<str:searchword>', views.search_title, name='search_title'),
]
