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

def main():
	rmtip = "10.136.60.2"
	usernm = "Administrator"
	passwd = "gsLab1234"
	currSession = winrm.Session(rmtip,auth=(usernm,passwd))
	getvm = currSession.run_cmd('wbadmin get virtualmachines')
	splitvm = getvm.std_out.split('\r\n\r\n')	#get individual vm tuples
	listVm(splitvm)
	global a
	a=filter(None,a)
	return a