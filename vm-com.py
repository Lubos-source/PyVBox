import virtualbox
import time

vbox = virtualbox.VirtualBox()

#print("VM(s):\n + %s" % "\n + ".join([vm.name for vm in vbox.machines]))


def listmachines():
    """ Working """
    listmach=[]
    vbox = virtualbox.VirtualBox()
    for vm in vbox.machines:
        listmach.append(vm.name)
    return listmach


def launchMachine(machine):
    """ Working """
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()
    vm = vbox.find_machine(machine)
    progress = vm.launch_vm_process(session, "gui", [])
    progress.wait_for_completion()
    #print(session.state)
    #print(progress.operation_percent)
    """ not needed thanks to : wait_for_completion()
    while progress.operation_percent<100:
        time.sleep(0.5)
        print(progress.operation_percent)
    """
    session.unlock_machine()
    #print(session.state)

def DownMachine():
    """ WORKING """
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine("Windows10")
    session=machine.create_session()
    #gs = session.console.guest.create_session("win10","")
    print(session.state)
    
    session.console.power_down()
    session.unlock_machine()
    print(session.state)

def Write():
    """ working """
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine('Windows10')
    session = vm.create_session()
    session.console.keyboard.put_keys("Q: \'You want control?\'\nA: \'Yes, but just a tad...\'\n")


def CopyFile():
    """ NOT WORKING YET """
    # Assume machine is already running.
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine("Windows10")
    session = machine.create_session()

    # copy notepad.exe to ./notepad.exe
    gs = session.console.guest.create_session("win10","") #"mick", "password"
    gs.file_copy_to_guest("C:\\Users\\lab\\Desktop\\notepad.exe", "C:\\Windows\\System32\\notepad.exe", [])
    gs.close()

def read_snapshot(mach_name, snap_name):
    """ WORKING """
    """ If running --> turn off and then do ! """
    start=time.time()
    vb=virtualbox.VirtualBox()
    session = virtualbox.Session()
    try:
        vm = vb.find_machine(mach_name)
        snap = vm.find_snapshot(snap_name)
        vm.create_session(session=session)
    except virtualbox.library.VBoxError as e:
        return print("failed", e.msg, True)
    except Exception as e:
        return print( "failed", str(e), True)

    restoring = session.machine.restore_snapshot(snap)

    while restoring.operation_percent < 100:
        time.sleep(0.5)

    session.unlock_machine()
    if restoring.completed == 1:
        return print("success", "restoring completed in {:>.4} sec".format(str(time.time() - start)), False)
    else:
        return print("failed", "restoring not completed", True)

def take_snapshot(machine_name,snapshotname,snap_description=""+str(time.time())+""):
    """ WORKING """
    machine = vbox.find_machine(machine_name)
    session=machine.create_session()
    process, unused_variable = session.machine.take_snapshot(snapshotname, snap_description, False)
    process.wait_for_completion(timeout=-1)
    session.unlock_machine()

machines=listmachines()

#launchMachine("Windows10")
#Write()
#read_snapshot("Windows10","snaptest1")
#take_snapshot("Windows10","Snap_Name_TESTING")
#DownMachine()




#CopyFile()
print(virtualbox.Session().state)
#print(virtualbox.Session())