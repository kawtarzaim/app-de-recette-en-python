from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.db.models import Q
from .models import Recipe, Rating
from .forms import RecipeForm


class RecipeListView(View):
    def get(self, request):
        qs = Recipe.objects.select_related('category', 'author').prefetch_related('tags')
        
        # Handle search query
        search_query = request.GET.get('q', '').strip()
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(ingredients__icontains=search_query)
            )
        
        # simple filters from GET
        category = request.GET.get('category')
        if category:
            qs = qs.filter(category__id=category)

        paginator = Paginator(qs.order_by('-created_at'), 9)
        page = request.GET.get('page', 1)
        recipes = paginator.get_page(page)

        # annotate simple rating info per object to use in template
        for r in recipes:
            ratings = r.ratings.all()
            r.ratings_count = ratings.count()
            r.average_rating = round(sum([ra.score for ra in ratings]) / ratings.count(), 1) if ratings.count() else 0

        active_filters = []
        if search_query:
            active_filters.append(f'Recherche: {search_query}')
        
        context = {
            'recipes': recipes,
            'categories': [],
            'tags': [],
            'active_filters': active_filters,
            'search_query': search_query,
        }
        return render(request, 'recettes/list.html', context)


class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        # compute ratings
        ratings = recipe.ratings.all()
        recipe.ratings_count = ratings.count()
        recipe.average_rating = round(sum([ra.score for ra in ratings]) / ratings.count(), 1) if ratings.count() else 0

        context = {'recipe': recipe}
        return render(request, 'recettes/detail.html', context)


@method_decorator(login_required, name='dispatch')
class RecipeCreateView(View):
    def get(self, request):
        form = RecipeForm()
        return render(request, 'recettes/create.html', {'form': form})

    def post(self, request):
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('recettes:detail', pk=recipe.pk)
        return render(request, 'recettes/create.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class RecipeEditView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.author != request.user:
            raise Http404("Vous ne pouvez pas modifier cette recette.")
        form = RecipeForm(instance=recipe)
        return render(request, 'recettes/edit.html', {'form': form, 'recipe': recipe})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.author != request.user:
            raise Http404("Vous ne pouvez pas modifier cette recette.")
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return redirect('recettes:detail', pk=recipe.pk)
        return render(request, 'recettes/edit.html', {'form': form, 'recipe': recipe})


@method_decorator(login_required, name='dispatch')
class MyRecipesView(View):
    def get(self, request):
        qs = Recipe.objects.filter(author=request.user).select_related('category').prefetch_related('tags')
        paginator = Paginator(qs.order_by('-created_at'), 9)
        page = request.GET.get('page', 1)
        recipes = paginator.get_page(page)

        for r in recipes:
            ratings = r.ratings.all()
            r.ratings_count = ratings.count()
            r.average_rating = round(sum([ra.score for ra in ratings]) / ratings.count(), 1) if ratings.count() else 0

        context = {
            'recipes': recipes,
            'categories': [],
            'tags': [],
            'active_filters': [],
        }
        return render(request, 'recettes/my_recipes.html', context)