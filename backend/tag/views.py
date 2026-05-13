from django.shortcuts import render
from .models import Tag

def list_view(request):
	tags = Tag.objects.all()
	return render(request, 'tag/list.html', {'tags': tags})
