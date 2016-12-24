from __future__ import unicode_literals
from django.db import models


class Profile(models.Model):
	vm=models.OneToOneField('VM',on_delete=models.CASCADE)
	full_count=models.IntegerField()
	diff_count=models.IntegerField()
	full_del_count=models.IntegerField()
	def __str__(self):
		return str(self.id)

class VM(models.Model):
	VM_name=models.CharField(max_length=1000, primary_key=True)
	VM_id=models.CharField(max_length=500, blank=True)
	hyper_type=models.CharField(max_length=1000,blank=True)
	state=models.CharField(max_length=5000,blank=True)
	backup_content=models.FileField(blank=True,null=True)
	disk_location=models.FilePathField(blank=True, null=True)
	guest_name=models.CharField(max_length=1000, blank=True, null=True)
	#owner = models.ForeignKey('auth.User', related_name='vm', on_delete=models.CASCADE, editable=False)
	#annotation=models.CharField(max_length=1000, blank=True)
	ip=models.CharField(max_length=100,blank=True,null=True)
	class Meta:
		ordering=('VM_name',)

	def __str__(self):
		return self.VM_name

	#def save(self, *args, **kwargs):
	    #super(VM, self).save(*args, **kwargs)


class Backup(models.Model):
	vm=models.ForeignKey('VM', on_delete=models.CASCADE, )
	VM_name=models.CharField(max_length=1000, )
	backup_name=models.CharField(max_length=1000, primary_key=True)
	status=models.CharField(max_length=1000, blank=True)
	#vm_ID=models.IntegerField()
	metadata=models.FileField(blank=True,)
	#timestamp=models.TimeField(auto_now_add=True,blank=True)	
	image=models.FileField(blank=True)

	def __str__(self):
		return str(self.backup_name)

	#def save(self, *args, **kwargs):
	 	#super(Backup, self).save(*args, **kwargs)

class DiffBackup(models.Model):
	backup=models.OneToOneField('Backup',on_delete=models.CASCADE)
	#backup_id=models.IntegerField()
	image=models.FileField(blank=True)
	timestamp=models.TimeField(auto_now_add=True)
	count=models.IntegerField()

	def __str__(self):
		return str(self.id)

"""class ListVM(models.Model):
	list_vm=[[]*2]
	i=0

	def increment_counter():
		i=i+1
	def append_list():
		list_vm.append([])"""
