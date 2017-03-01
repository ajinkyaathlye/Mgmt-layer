from rest_framework import serializers
from .models import VM, Backup, Profile, Jobs
from django.contrib.auth.models import User


class KVMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = ('VM_id', 'VM_name', 'hyper_type', 'state', 'guest_name', 'ip', 'profile')


class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = ('VM_id', 'hyper_type', 'state', 'profile')


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
