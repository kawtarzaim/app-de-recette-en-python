from django.urls import path
from .views import gallery_view

app_name = 'photo'

urlpatterns = [
    path('', gallery_view, name='gallery'),
]
