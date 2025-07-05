from django.contrib import admin
from .models import StudentProfile
from .models import ReferralRequest
from .models import Notification
from .models import Bookmark

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(ReferralRequest)
admin.site.register(Notification)
admin.site.register(Bookmark)
