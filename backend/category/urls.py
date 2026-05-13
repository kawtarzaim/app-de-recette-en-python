from django.urls import path
from .views import list_view, create_category

app_name = 'category'

urlpatterns = [
    path('', list_view, name='list'),
    path('create/', create_category, name='create'),
    path('<slug:slug>/', list_view, name='detail'),
]
