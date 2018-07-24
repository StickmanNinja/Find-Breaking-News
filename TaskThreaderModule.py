from threading import *
import os
import time
import linecache

# The 'data' argument needs to be a list with functions.
def runTasks(data):
    if type(data) is list and len(data) > 0:
        loop(data)
        return True
    else:
        return False

# Loops through data list, runs functions, then starts "finished()" when complete.
def loop(data):
    try:
        r = range(0, len(data))
        for x in r:
            # Initializes processes.
            locals()['TaskThreaderModuleloop%s' % x] = Thread(target=data[x])

        for x in r:
            # Starts processes.
            locals()['TaskThreaderModuleloop%s' % x].start()

        # Waits for functions to complete. 
        for x in r:
            locals()['TaskThreaderModuleloop%s' % x].join()
    except:
        PrintException()
