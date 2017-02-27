from rest_framework import serializers
from .models import VM, Backup, Profile, Jobs
from django.contrib.auth.models import User

class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = "__all__"


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('VM_name', 'backup_name', 'status')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"
