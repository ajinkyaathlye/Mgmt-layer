from rest_framework import serializers
from .models import VM, Backup
from django.contrib.auth.models import User

"""class VMSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = VM
		fields = '__all__'
		#owner = serializers.ReadOnlyField(source='owner.username')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    vm = serializers.HyperlinkedRelatedField(many=True, view_name='vm-detail', read_only=True)

    class Meta:
        model = User
        fields = '__all__'	"""

class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = "__all__"

class BackupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Backup
        fields = ('VM_name','backup_name')