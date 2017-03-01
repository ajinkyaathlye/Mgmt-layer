import threading
import time
import atexit

global exitFlag
from . import policy_script


def exitnow():
    global exitFlag
    print exitFlag
    exitFlag = 1


class Policy(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        time.sleep(10)
        i = 0;
        while (True):
            global exitFlag
            if exitFlag != 0:
                self._is_running = False
                break
            else:
                policy_script.main()
            time.sleep(90)


exitFlag = 0


# Create new threads

def main():
    thread1 = Policy(1, "Policy Thread")
    atexit.register(exitnow)
    try:
        thread1.start()
        # time.sleep(10)
        print "Exiting Main Thread"
    except (SystemExit):
        print exitFlag
        exitFlag = 1
