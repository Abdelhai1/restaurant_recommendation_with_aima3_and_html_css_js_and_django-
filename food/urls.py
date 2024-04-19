from django.urls import path
from .views import  restaurant_recommendation

urlpatterns = [
    path('', restaurant_recommendation, name='restaurant_recommendation'),
]
