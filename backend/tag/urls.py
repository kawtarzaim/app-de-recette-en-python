from django.urls import path
from .views import list_view

app_name = 'tag'

urlpatterns = [
    path('', list_view, name='list'),
    path('<slug:slug>/', list_view, name='detail'),
]
