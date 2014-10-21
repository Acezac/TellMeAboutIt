from django.contrib import admin
from TellMeAboutIt_BL.models import UserProfile, Comment, Complaint


admin.site.register(UserProfile)
admin.site.register(Complaint)
admin.site.register(Comment)

