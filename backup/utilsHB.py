from __future__ import print_function
import winrm  # install library by: pip install pywinrm


def main(rmtip, usernm, passwd, bckDest):
    # rmtip = "10.136.60.2"
    # usernm = "Administrator"
    # passwd = "gsLab1234"

    # print "\nRemote machine :: 10.136.60.2\nUsername :: Administrator"
    # print "Can modify auth details as needed\n"

    # add as trusted host on both machines
    # allowUnencrypted = True
    print ("asdasd")
    currSession = winrm.Session(rmtip, auth=(usernm, passwd))

    # bckDest = raw_input("Enter the VM destination drive letter: ")
    # get
    getVer = "wbadmin get versions -backuptarget:" + bckDest + ":"
    # print "Existing Backup files: \n"
    runCmd = currSession.run_cmd(getVer)  # display all existing backups on the drive

    # have to group all VM data together
    splitvm = runCmd.std_out.split('\r\n\r\n')  # indivisual vm data

    nameVerList = []

    for currvm in splitvm:
        linesvm = currvm.split('\r\n')
        for currline in linesvm:
            wordsvm = currline.split(': ')
            if (wordsvm[0] == 'Version identifier'):
                l = []
                verNu = wordsvm[1]  # extra data for all versions
                verNu = verNu.replace(" ", "")
                l.append(verNu)

                infoVer = "wbadmin get items -version:" + verNu + " -backuptarget:" + bckDest + ":"
                runCmd = currSession.run_cmd(infoVer)
                vmVerData = runCmd.std_out.split('.\r\n\r\n')

                vmVerLines = vmVerData[1].split('\r\n')

                for vmVerPara in vmVerLines:
                    lineParams = vmVerPara.split(': ')
                    if (lineParams[0] == 'VM name'):
                        lineParams[1] = lineParams[1].replace(" ", "")
                        l.append(lineParams[1])
                nameVerList.append(l)
    print (nameVerList)
    print ("ajinkya")
    return nameVerList
