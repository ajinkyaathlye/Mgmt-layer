import winrm	#install library by: pip install pywinrm

a=[]

def listVm(splitvm):
	global a
	for currvm in splitvm:
		l=[]
		linesvm = currvm.split('\r\n')		#line by line slice
		for currline in linesvm:
			wordsvm = currline.split(': ')	#slicing each parameter
			if(wordsvm[0]=='VM name'):
				l.append(wordsvm[1])
				#print wordsvm[1]
			if(wordsvm[0]=='VM caption'):
				l.append(wordsvm[1])
				#print wordsvm[1]
			if(wordsvm[0]=='VM identifier'):
				l.append(wordsvm[1])
				#print wordsvm[1]
		a.append(l)

def main(rmtip, usernm, passwd):
	#rmtip = "10.136.60.33"
	#usernm = "Administrator"
	#passwd = "gsLab@123"
	print rmtip[0], usernm[0], passwd[0]	
	currSession = winrm.Session(rmtip[0],auth=(usernm[0],passwd[0]))
	getvm = currSession.run_cmd('wbadmin get virtualmachines')
	splitvm = getvm.std_out.split('\r\n\r\n')	#get individual vm tuples
	listVm(splitvm)
	global a
	a=filter(None,a)
	print a
	return a