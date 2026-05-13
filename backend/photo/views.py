from django.shortcuts import render

def gallery_view(request):
	photos = []
	return render(request, 'photo/gallery.html', {'photos': photos})
