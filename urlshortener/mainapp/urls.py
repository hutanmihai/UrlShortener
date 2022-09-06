from django.urls import path
from .views import *

urlpatterns = [
    path('', index_handler, name='index'),
    path('link/<str:short_url>', link_handler, name='link'),
    path('register', register_handler, name='register'),
]
