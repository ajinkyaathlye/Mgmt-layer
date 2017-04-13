from .models import VM, Backup, Profile, Jobs
from .serializers import KVMSerializer, ESXSerializer, HyperVSerializer, BackupSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from . import models, utils, utilsH, utilsK, utilsKB, utilsHB, backup_kvm, backup_hyperv, backup_esx, \
    restore_esx, restore_kvm, restore_hyperv
import pdb, datetime
import logging

@api_view(['GET', 'POST'])
def vm_list(request, hv, util, ip, password, user, vmname, bkupid=None, restoreName=None, format=None):
    logger = logging.getLogger('log')
    if util == 'backup':
        if request.method == 'GET':
            if hv == "kvm":
                l = []
                list_VM = utilsK.main(ip, user, password)
                print list_VM
                for vm in list_VM:
                    # d = models.Details(hyper_type='KVM', ip_addr=ip, username=user, password=password)
                    db, created = models.Details.objects.get_or_create(hyper_type='KVM', ip_addr=ip, username=user,
                                                                       password=password)
                    # print db
                    # print created
                    print created
                    if created == False:
                        db.save()
                        #print "HAHAHAHA"
                    virt_mach, flag = VM.objects.get_or_create(VM_name=vm[1],
                                                               details=db,
                                                               VM_id=vm[0],
                                                               hyper_type="KVM",
                                                               #state=vm[2],
                                                               guest_name="",
                                                               ip=ip,
                                                               )
                    if flag == False:
                        virt_mach.state=vm[2]
                        virt_mach.save()
                    zz = models.VM.objects.get(VM_name=vm[1]);
                    print zz.profile, "========================", zz.VM_id
                    vms = VM.objects.get(hyper_type="KVM", VM_id=vm[0])
                    l.append(vms)
                serializer = KVMSerializer(l, many=True)
                return Response(serializer.data)

            elif hv == "esx":
                # ip="192.168.32.98"
                # password="gsLab123"
                # user="sumitt@ad2lab.com"
                list_VM = utils.main(ip, password, user)
                # print "IN VMLIST"
                l = []
                for vm in list_VM:
                    # d = models.Details(hyper_type='KVM', ip_addr=ip, username=user, password=password)
                    db, created = models.Details.objects.get_or_create(hyper_type='ESX', ip_addr=ip, username=user,
                                                                       password=password)
                    # print db
                    # print created

                    if created == False:
                        db.save()
                    if vm is not None:
                        virt_mach, flag = VM.objects.get_or_create(VM_id=vm[0],
                                                                   details=db,
                                                                   VM_name=vm[0],
                                                                   hyper_type="ESX",
                                                                   guest_name=vm[2],
                                                                   state=vm[3],
                                                                   ip=vm[4],
                                                                   )
                    if flag == False:
                        virt_mach.save()
                    vms = VM.objects.get(hyper_type="ESX", VM_id=vm[0])
                    l.append(vms)
                serializer = ESXSerializer(l, many=True)
                return Response(serializer.data)

            elif hv == "hyperv":
                l = []
                list_VM = utilsH.main(ip, user, password)
                # print "hgfhgfhgf", list_VM
                for vm in list_VM:
                    # d = models.Details(hyper_type='KVM', ip_addr=ip, username=user, password=password)
                    db, created = models.Details.objects.get_or_create(hyper_type='HyperV', ip_addr=ip, username=user,
                                                                       password=password)
                    if created == False:
                        db.save()
                    if vm is not None:
                        virt_mach, flag = VM.objects.get_or_create(VM_name=vm[0],
                                                                   details=db,
                                                                   VM_id=vm[0],
                                                                   hyper_type="HyperV",
                                                                   guest_name="",
                                                                   ip="",
                                                                   state=vm[1],
                                                                   )
                        if flag == False:
                            virt_mach.save()
                    vms = VM.objects.get(hyper_type="HyperV", VM_id=vm[0])
                    print vms.profile
                    l.append(vms)
                serializer = HyperVSerializer(l, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if hv == "kvm":
                vm = VM.objects.get(VM_id=request.data['VM_name'])
                j = Jobs(vm=vm,
                         status='IN PROGRESS',
                         function='Backup',
                         timestamp=datetime.datetime.now(),
                         hyper_type='KVM')
                j.save()
                bkupserializer = BackupSerializer(data=request.data)
                # print request.data
                if bkupserializer.is_valid():
                    try:
                        bkupID = backup_kvm.main(ip, request.data['backup_name'], request.data['VM_name'],
                                                 vm.profile.freq_count, user, password)
                        Backup(vm=vm,
                               backup_name=request.data['backup_name'],
                               bkupid=bkupID,
                               VM_name=str(request.data['VM_name']),
                               ).save()
                        j.status = 'COMPLETED'
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        logger.info(Response(bkupserializer.data, status=status.HTTP_201_CREATED))
                        return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        print e
                        j.status = 'FAILED: ' + e
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        logger.info(Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR))
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # print request.data
                else:
                    j.status = 'FAILED'
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(bkupserializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if hv == "esx":
                vm = VM.objects.get(VM_id=request.data['VM_name'])
                j = Jobs(vm=vm,
                         status='IN PROGRESS',
                         function='Backup',
                         timestamp=datetime.datetime.now(),
                         hyper_type='ESX')
                j.save()
                bkupserializer = BackupSerializer(data=request.data)
                if bkupserializer.is_valid():
                    try:
                        backup_esx.main(ip, password, user, request.data['VM_name'], request.data['backup_name'],
                                        vm.profile.freq_count)
                        Backup(vm=vm,
                               backup_name=request.data['backup_name'],
                               VM_name=request.data['VM_name'],
                               ).save()
                        j.status = 'COMPLETED'
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        print e
                        j.status = 'FAILED: ' + e
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    j.status = 'FAILED'
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(bkupserializer.data, status=status.HTTP_400_BAD_REQUEST)

            if hv == "hyperv":
                vm = VM.objects.get(VM_id=str(request.data['VM_name']))
                j = Jobs.objects.get_or_create(vm=vm,
                         status='IN PROGRESS',
                         function='Backup',
                         timestamp=datetime.datetime.now(),
                         hyper_type='HyperV')
                bkupserializer = BackupSerializer(data=request.data)
                if bkupserializer.is_valid():
                    try:
                        verList = backup_hyperv.main(ip, password, user, request.data['VM_name'], vm.profile.freq_count)
                        Backup(vm=vm,
                               backup_name=request.data['backup_name'],
                               bkupid=verList[0],
                               destination=verList[1],
                               VM_name=str(request.data['VM_name']),
                               ).save()
                        j.status = 'COMPLETED'
                        flag = 0
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        print e
                        j.status = 'FAILED: ' + e
                        j.timestamp = datetime.datetime.now()
                        j.save()
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    j.status = 'FAILED'
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(bkupserializer.data, status=status.HTTP_400_BAD_REQUEST)



    elif util == 'restore':
        if request.method == 'GET':
            if hv == "kvm":
                openstackbkups = utilsKB.main(ip, user, password, vmname)
                vm_obj = VM.objects.get(VM_id=vmname)
                print "=================================="
                dict = {}
                for bkps in openstackbkups:
                    dict[bkps[0]] = bkps[2]
                # list_bkups = utilsKB.main(ip, user, password, vmname)
                # print ip, user, password, vmname
                backups = Backup.objects.filter(vm=vm_obj)
                for bk in backups:
                    if (bk.bkupid in dict):
                        bk.status = dict[bk.bkupid]
                    else:
                        bk.status = 'UNAVAILABLE'
                serializer = BackupSerializer(backups, many=True)
                return Response(serializer.data)

            elif hv == "hyperv":
                # pdb.set_trace()
                bkuplist = utilsHB.main(ip, user, password, 'D')
                vm_obj = VM.objects.get(VM_name=vmname)
                backups = Backup.objects.filter(vm=vm_obj)
                for bk in backups:
                    bk.status = 'ACTIVE'
                print "VM NAME: " + backups[0].vm.VM_id
                serializer = BackupSerializer(backups, many=True)
                return Response(serializer.data)

            elif hv == "esx":
                # pdb.set_trace()
                print "VM NAME: " + vmname
                #bkuplist = utilsEB.main(ip, password, user, vmname)
                vm_obj = VM.objects.get(VM_name=vmname)
                backups = Backup.objects.filter(vm=vm_obj)
                for bk in backups:
                    bk.status = 'ACTIVE'
                # print "VM NAME: " + backups[0].vm.VM_id
                serializer = BackupSerializer(backups, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if hv == "kvm":
                try:
                    vm = VM.objects.get(VM_id=vmname)
                    j = Jobs(vm=vm,
                             status='IN PROGRESS',
                             function='Restore',
                             timestamp=datetime.datetime.now(),
                             hyper_type='KVM')
                    j.save()
                    resp = restore_kvm.main(ip, user, password, vmname, bkupid, restoreName)
                    j.status = 'COMPLETED'
                    j.timestamp=datetime.datetime.now()
                    j.save()
                    return Response(resp, status=status.HTTP_201_CREATED, )
                except Exception as e:
                    print e
                    j.status = 'FAILED: ' + e
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if hv == "esx":
                try:
                    vm = VM.objects.get(VM_id=vmname)
                    print "IN API++++++++++++++" + vm.VM_id
                    j = Jobs(vm=vm,
                             status='IN PROGRESS',
                             function='Restore',
                             timestamp=datetime.datetime.now(),
                             hyper_type='ESX')
                    j.save()
                    resp = restore_esx.main(ip, password, user, vmname, bkupid)
                    j.status = 'COMPLETED'
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(status=status.HTTP_201_CREATED)
                except Exception as e:
                    print e
                    j.status = 'FAILED' + e
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if hv == "hyperv":
                # pdb.set_trace()
                try:
                    vm = VM.objects.get(VM_id=vmname)
                    j = Jobs(vm=vm,
                             status='IN PROGRESS',
                             function='Restore',
                             timestamp=datetime.datetime.now(),
                             hyper_type='HyperV')
                    j.save()
                    restore_hyperv.main(ip, user, password, vmname, bkupid,
                                        'D')
                    j.status = 'COMPLETED'
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(status=status.HTTP_201_CREATED)
                except Exception as e:
                    print e
                    j.status = 'FAILED' + e
                    j.timestamp = datetime.datetime.now()
                    j.save()
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def createPolicy(request, startDay, startMonth, startYear, endDay, endMonth, endYear, bckrotation, policyName,  format=None):
    if request.method == 'GET':
        flag=0
        d = models.Profile()
        d.start_date = datetime.date(int(startYear), int(startMonth), int(startDay))
        d.end_date = datetime.date(int(endYear), int(endMonth), int(endDay))
        d.freq_count = int(bckrotation)
        d.del_count = 4
        d.name = policyName
        list=Profile.objects.all()
        print list
        print policyName
        for i in list:
            print i.name
            if(i.name == policyName):
                raise Exception("Policy Exists")
        d.save()
        serializer = ProfileSerializer(d)
        return Response(serializer.data)


def conPolicy(request, policyName, vmID):
    policy = Profile.objects.get(name=policyName)
    vm = VM.objects.get(VM_id=vmID)
    vm.profile = policy
    vm.save()


@api_view(['GET', 'PUT', 'DELETE'])
def vm_detail(request, hv, name, format=None):
    try:
        vm = VM.objects.get(hyper_type=hv, VM_name=name)
    except VM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VMSerializer(vm)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VMSerializer(vm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# def set_policy(request):
"""
string=""
@api_view(['GET', 'POST'])
def getHv(request, hv):
	if request.method=='GET':
		self.string=hv
class VMViewSet(viewsets.ModelViewSet):
	if string == "kvm":
	    vms=VM()
        list_VM = utilsK.main()
    	for vm in list_VM:
    		vm = VM(VM_name=vm[1],
    			VM_id=vm[0],
    			hyper_type="KVM",
    			state=vm[2],
    			disk_location="",
    			guest_name="",
    			ip="",
    			backup_content="",
    			).save()
    	vms = VM.objects.filter(hyper_type="KVM")
    	queryset = vms
    	serializer_class = VMSerializer
    	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      		IsOwnerOrReadOnly,)
	if string == "esx":
	    vms=VM()
        list_VM = utilsK.main()
    	for vm in list_VM:
    		VM(VM_name=vm[0],
    			hyper_type="ESX",
    			disk_location=vm[1],
    			guest_name=vm[2],
    			state=vm[3],
    			ip=vm[4],
    			backup_content="",
    			).save()
    	vms=VM.objects.filter(hyper_type="ESX")
    	queryset = vms
    	serializer_class = VMSerializer
    	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      		IsOwnerOrReadOnly,)
	if string == "hyperv":
	    vms=VM()
        list_VM = utilsK.main()
    	for vm in list_VM:
    		if vm is not None:
	    		VM(VM_name=vm[0],
    			hyper_type="HyperV",
    			disk_location="",
    			guest_name="",
    			ip="",
    			backup_content="",
    			state=vm[1],
    			).save()
    	vms=VM.objects.filter(hyper_type="HyperV")
    	queryset = vms
    	serializer_class = VMSerializer
    	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      		IsOwnerOrReadOnly,)
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer"""
