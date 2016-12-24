from .models import VM, Backup
from .serializers import VMSerializer, BackupSerializer
from django.contrib.auth.models import User
#from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework import status
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models, utils, utilsH, utilsK, utilsKB, utilsEB, utilsHB, backup_kvm, backup_hyperv, backup_esx, restore_esx, restore_kvm, restore_hyperv
import pdb

@api_view(['GET', 'POST'])
def vm_list(request, hv, util, format=None):
    if util == 'backup':
        if request.method == 'GET':
       	    if hv == "kvm":
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
    	       	serializer = VMSerializer(vms, many=True)
    	    	return Response(serializer.data)

    	    elif hv=="esx":
    	    	list_VM = utils.main()
    	    	for vm in list_VM:
    	    		if vm is not None:
    		    		VM(VM_name=vm[0], 
    	    			hyper_type="ESX",
    	    			disk_location=vm[1],
    	    			guest_name=vm[2],
    	    			state=vm[3],
    	    			ip=vm[4],
    	    			backup_content="",
    	    			).save()
    	    	vms=VM.objects.filter(hyper_type="ESX")
    	       	serializer = VMSerializer(vms, many=True)
    	        return Response(serializer.data)

    	    elif hv=="hyperv":
    	    	list_VM = utilsH.main()
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
    	       	serializer = VMSerializer(vms, many=True)
    	        return Response(serializer.data)

        elif request.method == 'POST':
            if hv == "kvm":
                bkupserializer = BackupSerializer(data=request.data)
                if bkupserializer.is_valid():
                    vm=VM.objects.get(VM_name=str(request.data['VM_name']))
                    bkuplist=backup_kvm.main(str(request.data['backup_name']))
                    Backup(vm=vm,
        	    	backup_name=str(bkuplist[0]),
        	    	#backup_id=str(bkuplist[1]),
                    #VM_name=str(request.data['VM_name']),
        	    	#status=str(bkuplist[2]),
        	    	).save()
                    return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(bkupserializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if hv == "esx":
                bkupserializer = BackupSerializer(data=request.data)
                if bkupserializer.is_valid():
                    vm=VM.objects.get(VM_name=str(request.data['VM_name']))
                    backup_esx.main(str(request.data['VM_name']), str(request.data['backup_name']))
                    Backup(vm=vm,
                    backup_name=str(request.data['backup_name']),
                    ).save()
                    return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(bkupserializer.data, status=status.HTTP_400_BAD_REQUEST)

            if hv == "hyperv":
                bkupserializer = BackupSerializer(data=request.data)
                if bkupserializer.is_valid():
                    vm=VM.objects.get(VM_name=str(request.data['VM_name']))
                    backup_hyperv.main(str(request.data['VM_name']))
                    Backup(vm=vm,
                    backup_name="",
                    ).save()
                    return Response(bkupserializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(bkupserializer.data, status=status.HTTP_400_BAD_REQUEST)



    elif util == 'restore':
        if request.method == 'GET':
            if hv == "kvm":
                vm_obj=VM.objects.get(VM_name=str(request.data['VM_name']))
                list_bkups = utilsKB.main()
                for bkup in list_bkups:
                    Backup(vm=vm,
                    backup_name=str(bkuplist[1]),
                    backup_id=str(bkuplist[0]),
                    VM_name=str(request.data['VM_name']),
                    status=str(bkuplist[2]),
                    ).save()
                bkups = Backup.objects.filter(vm=vm_obj)
                serializer = BackupSerializer(bkups, many=True)
                return Response(serializer.data)

            elif hv=="esx":
                bkuplist = utilsEB.main('test_TSAM')
                vm_obj=VM.objects.get(VM_name='test_TSAM')
                for bkup in bkuplist:
                    if bkup is not None:
                        Backup(vm=vm_obj,
                        backup_name=str(bkup[0]),
                        VM_name='test_TSAM'
                        ).save()
                backups=Backup.objects.filter(vm=vm_obj)
                serializer = BackupSerializer(backups, many=True)
                return Response(serializer.data)

            elif hv=="hyperv":
                #pdb.set_trace()
                bkuplist = utilsHB.main('D')
                for bkup in bkuplist:
                    if bkup is not None:
                        vm_obj=VM.objects.get(VM_name=bkup[1])
                        Backup(vm=vm_obj,
                        backup_name=str(bkup[0]),
                        VM_name=str(bkup[1]),
                        ).save()
                backups=Backup.objects.all()
                serializer = BackupSerializer(backups, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if hv == "kvm":
                restore_kvm.main(str(request.data['VM_name']), str(request.data['backup_name']))
                return Response(status=status.HTTP_201_CREATED)

            if hv == "esx":
                #pdb.set_trace()
                #bkupserializer = BackupSerializer(data=request.data)
                #if bkupserializer.is_valid():
                restore_esx.main(str(request.data['VM_name']), str(request.data['backup_name']))
                return Response(status=status.HTTP_201_CREATED)
                #else:
                   # return Response(bkupserializer.data, status=status.HTTP_400_BAD_REQUEST)

            if hv == "hyperv":
                #pdb.set_trace()
                restore_hyperv.main('D', str(request.data['backup_name']), str(request.data['VM_name']))  
                return Response(status=status.HTTP_201_CREATED)

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

