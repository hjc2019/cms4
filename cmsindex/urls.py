from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('articleContent/', views.articleContent),
    path('articleClassifiedList/', views.articleClassifiedList),
    path('positionNews/', views.positionNews),
]