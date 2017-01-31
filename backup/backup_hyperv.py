import winrm	#install library by: pip install pywinrm

#rmtip = "10.136.60.2"
#usernm = "Administrator"
#passwd = "gsLab1234"

#print "\nRemote machine :: 10.136.60.2\nUsername :: Administrator"
#print "Can modify auth details as needed\n"

	#add as trusted host on both machines
	#allowUnencrypted = True


def backup(rmtip, passwd, usernm, VMname):
	#print rmtip
	currSession = winrm.Session(rmtip[0],auth=(usernm[0],passwd[0]))
	#vvdUb = vmname

	#vmname = raw_input("Enter VM name to backup: ")
	#bckdest = raw_input("Enter destination drive letter: ")
	vmname = VMname
	bckdest = "D"
	bckcmd = "wbadmin start backup -backuptarget:"+bckdest+": -hyperv:\""+vmname+"\" -vssfull -quiet"
		#yet to figure out how to dynamically show command run info..

	#print "May take 5-10 minutes.. Please wait..\n\n"

	runcmd = currSession.run_cmd(bckcmd)

	#print runcmd.status_code
	#print runcmd.std_out

	if(runcmd.status_code == 4294967293):		#error wrong name
		print "VM: \""+vmname+"\" not found"
	if(runcmd.status_code == 4294967294):		#error wrong dest
		print "Destination: \""+bckdest+"\" not found"
	if(runcmd.status_code == 0):		#correct exec
		print "VM: \""+vmname+"\" has been backed up"

def main(rmtip, passwd, usernm, VMname):
	backup(rmtip, passwd, usernm, VMname)