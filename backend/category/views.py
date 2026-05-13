from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Category
from .forms import CategoryForm


def list_view(request):
    categories = Category.objects.all()
    # attach recipe_count if available via relationship - safe default 0
    for c in categories:
        c.recipe_count = getattr(c, 'recipe_count', 0)
    return render(request, 'category/list.html', {'categories': categories})


def is_admin(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:list')
    else:
        form = CategoryForm()
    return render(request, 'category/create.html', {'form': form})

