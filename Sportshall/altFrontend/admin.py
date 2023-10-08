from django.contrib import admin
from django.apps import apps

# Register your models here.
alt_frontend_models = apps.get_app_config('altFrontend').get_models()

for model in alt_frontend_models:
    admin.site.register(model)