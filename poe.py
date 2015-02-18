#Michael Quinn Parkinson - POE MACRO SCRIPT
# This program will open Path of exile via steam or directly from the .exe.
# Everything in this program is legal to use within POE.
# Each option is initiated once via human action i.e. 
# pressing the tilda (~), f4, or f5 keys.
# The program takes control of the keyboard and mouse for a 
#brief moment will executing the tasks.


#Some bugs include simutaniously hitting f4 or f5 while typing.
# The Time it takes to execute a task can be reduced.


################################################################################
# Auto Open, Instant Alt-F4, /OOS, and /REMAINING for Path Of Exile (Windows 7)
################################################################################
try:
    import os
    import subprocess
    from pymouse import PyMouse
    from pykeyboard import PyKeyboard
    import time
    import random
    import win32gui
    import win32con
    import win32api
    import ctypes
    import win32pdh
    import string
    import win32api
    import msvcrt
except ImportError:
    print "\nMissing Modules\n"
################################################################################
################################################################################
## Opens Path Of Exile
## The Tilda Key Is Alt-F4
## F4 Is /remaining
## F5 Is /oos
################################################################################
# k and m are the keyboard and mouse controllers
################################################################################
k = PyKeyboard()
m = PyMouse()
################################################################################
# Finds the location of the path of exile.exe steam and non steam
# Once the location is found the program is opened
# May take a while to iterate through computer
################################################################################
def RunPOE():
    folder = "C:\Program Files (x86)"
    file_list = []
    for (paths, dirs, files) in os.walk(folder):
        for file in files:
            if (file == 'PathOfExileSteam.exe') or (file == 'Path Of Exile.exe'):
                file_list.append(os.path.join(paths))
                file_name = file
    os.chdir(file_list[0])
    args = [file_name]
    p = subprocess.Popen(args)
    return p
################################################################################
# Searches through the process array and closes the path of exile process
################################################################################
def CloseProgram():
    for row in procids():
        if (row[0] == 'PathOfExileSteam') or (row[0] == 'PathOfExile'):
            os.kill(int(row[1]),9)
        else:
            continue
################################################################################
# Hits enter types /oos then hits enter
################################################################################
def OOS():
    k.tap_key('\n',repeat = 1)
    time.sleep(random.uniform(0,0.2))
    k.type_string('/oos')
    time.sleep(random.uniform(0,0.2))
    k.tap_key('\n',repeat = 1)
################################################################################
# Hits enter types /remaining then hits enter
################################################################################
def Remaining():
    k.tap_key('\n',repeat = 1)
    time.sleep(random.uniform(0,0.2))
    k.type_string('/remaining')
    time.sleep(random.uniform(0,0.2))
    k.tap_key('\n',repeat = 1)
################################################################################
# Searches for every running process then creates an array
################################################################################
def procids():
    junk, instances = win32pdh.EnumObjectItems(None,None,'process',
                                               win32pdh.PERF_DETAIL_WIZARD)
    proc_ids=[]
    proc_dict={}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance]=0
    for instance, max_instances in proc_dict.items():
        for inum in xrange(max_instances+1):
            hq = win32pdh.OpenQuery()
            path = win32pdh.MakeCounterPath( (None,'process',instance,
                                              None, inum,'ID Process') )
            counter_handle=win32pdh.AddCounter(hq, path) 
            win32pdh.CollectQueryData(hq)
            type, val = win32pdh.GetFormattedCounterValue(counter_handle,
                                                          win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance,str(val)))
            win32pdh.CloseQuery(hq) 
    proc_ids.sort()
    return proc_ids
################################################################################
# State variables that determine if a button is hit
################################################################################
key_state = 2
sync_state = 2
remain_state = 2
progress = 0
################################################################################
# Infinite Loop that checks of a button is pressed 
################################################################################
while True:
    ## Starts POE    
    if progress == 0:
        p = RunPOE()
        progress += 1
    ## Various In Game Hotkeys
    if progress == 1:
        ## Check if Remaining is Pressed    
        remain_state = win32api.GetKeyState(0x73)
        if remain_state < -1:
            Remaining()
        ## Check if Sync is Pressed    
        sync_state = win32api.GetKeyState(0x74)
        if sync_state < -1:
            OOS()
        ## Check if Alt-F4 is Pressed    
        key_state = win32api.GetKeyState(192)
        if key_state < -1:
            CloseProgram()
            break
        else:
            continue
    else:
        continue
