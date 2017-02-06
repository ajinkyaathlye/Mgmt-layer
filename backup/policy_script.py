from . import models, backup_kvm
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_KVM():
	vms_kvm=models.VM.objects.filter(hyper_type='KVM')
	d=datetime.today()
	for vm in vms_kvm:
		if d>=vm.profile.start_date and d<=vm.profile.end_date:
			l=models.Backup.objects.filter(vm=vm).order_by('timestamp')
			for backup in l:
				if backup.timestamp==d:
					pass
				else:
					apis.vm_list(request, "KVM", "backup", vm.details.ip_addr, vm.details.password, vm.details.username)

def check_ESX():
	vms_esx=models.VM.objects.filter(hyper_type='ESX')
	d=datetime.today()
	for vm in vms_esx:
		if d>=vm.profile.start_date and d<=vm.profile.end_date:
			l=models.Backup.objects.filter(vm=vm).order_by('timestamp')
			for backup in l:
				if backup.timestamp==d:
					pass
				else:
					curl "http://127.0.0.1:8000/vm/esx/list/servip=192.168.32.98&servpaswd=gsLab123&servuser=sumitt@ad2lab.com"


def main():
	check_KVM()
