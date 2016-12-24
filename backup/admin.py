from django.contrib import admin
from .models import VM, Profile, Backup, DiffBackup

admin.site.register(VM)
admin.site.register(Profile)
admin.site.register(Backup)
admin.site.register(DiffBackup)
