from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.ImageListView.as_view(), name='dzi-image-list'),
    path('populate/', views.populate_from_data_json, name='populate-from-json'),
]