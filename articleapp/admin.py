from django.contrib import admin

from .models import ArticleProfile
from .models import VacancyPost

# Register your models here.
admin.site.register(ArticleProfile)
admin.site.register(VacancyPost)