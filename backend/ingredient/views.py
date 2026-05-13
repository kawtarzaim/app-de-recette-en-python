from django.shortcuts import render

def list_view(request):
	# If you have an Ingredient model, replace this with a real query
	ingredients = []
	return render(request, 'ingredient/list.html', {'ingredients': ingredients})
