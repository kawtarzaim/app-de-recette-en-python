from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView, RecipeEditView, MyRecipesView

app_name = 'recettes'

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='detail'),
    path('create/', RecipeCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', RecipeEditView.as_view(), name='edit'),
    path('my/', MyRecipesView.as_view(), name='my_recipes'),
    path('favorite/<int:pk>/', RecipeListView.as_view(), name='favorite_toggle'),
    path('search/', RecipeListView.as_view(), name='search'),
]
