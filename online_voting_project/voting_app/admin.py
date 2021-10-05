from django.contrib import admin

from .models import ContestantsDetail, StudentsRegistration, VoteVerification
# Register your models here.

admin.site.register(ContestantsDetail)
admin.site.register(StudentsRegistration)
admin.site.register(VoteVerification)
