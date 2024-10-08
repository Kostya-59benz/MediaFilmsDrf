from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor, Review
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter
# from .permissions import IsSuperUser


class MovieListView(generics.ListAPIView):

    filter_backends = (DjangoFilterBackend,)

    serializer_class = MovieListSerializer
    filterset_class = MovieFilter    


    def get_queryset(self):

        movies = Movie.objects.filter(draft=False).annotate(  
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))).annotate(
                middle_star = models.Sum(models.F('ratings__star')) /  models.Count(models.F('ratings'))
            )
        
        return movies

class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


# class ReviewDestroy(generics.DestroyAPIView):
#     """Удаление отзыва"""
#     queryset = Review.objects.all()
#     serializer_class = ReviewCreateSerializer
#     permission_classes = [IsSuperUser]


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer