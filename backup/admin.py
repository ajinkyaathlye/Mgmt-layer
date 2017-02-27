from django.contrib import admin
from .models import VM, Profile, Backup, DiffBackup, Details, Jobs

admin.site.register(VM)
admin.site.register(Profile)
admin.site.register(Backup)
admin.site.register(DiffBackup)
admin.site.register(Details)
admin.site.register(Jobs)
