from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

# Register all models from this app so they appear in the admin panel
app_config = apps.get_app_config('ingredient')

for model in app_config.get_models():
	try:
		admin.site.register(model)
	except AlreadyRegistered:
		pass
