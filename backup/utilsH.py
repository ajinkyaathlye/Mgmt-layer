import winrm  # install library by: pip install pywinrm

a = []


def listVm(splitvm):
    global a
    a = []
    for i in range(0, len(splitvm)-1):
        l = []
        currvm=splitvm[i]
        linesvm = currvm.split('\r\n')  # line by line slice
        for currline in linesvm:
            wordsvm = currline.split(': ')  # slicing each parameter
            if (wordsvm[0] == 'VM name'):
                l.append(wordsvm[1])
            # print wordsvm[1]
            if (wordsvm[0] == 'VM caption'):
                l.append(wordsvm[1])
            # print wordsvm[1]
            if (wordsvm[0] == 'VM identifier'):
                l.append(wordsvm[1])
                # print wordsvm[1]
        a.append(l)


def main(rmtip, usernm, passwd):
    # rmtip = "10.136.60.33"
    # usernm = "Administrator"
    # passwd = "gsLab@123"
    print rmtip, usernm, passwd
    currSession = winrm.Session(rmtip, auth=(usernm, passwd))
    getvm = currSession.run_cmd('wbadmin get virtualmachines')
    splitvm = getvm.std_out.split('\r\n\r\n')  # get individual vm tuples
    global a
    listVm(splitvm)
    a = filter(None, a)
    a=a[:len(a)-1]
    print a
    return a
