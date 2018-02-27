from django.contrib import admin
from .models import Profile, Course, Note, Enrollment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Note)
admin.site.register(Enrollment)
