from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('article/<int:id>/', views.detail_article, name='detail_article'),
    path('evenements/', views.liste_evenements, name='liste_evenements'),
    path('evenements/<int:id>/', views.detail_evenement, name='detail_evenement'),
]