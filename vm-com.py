import virtualbox
import time
import os

import subprocess

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
    """ Maybe rework to save current state and not just shutdown """
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine("Windows10")
    session=machine.create_session()
    #gs = session.console.guest.create_session("win10","")
    print(session.state)
    
    session.console.power_down()
    session.unlock_machine()
    print(session.state)

def Write(mach_name):
    """ Working """
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(mach_name)
    session = vm.create_session()
    """ try to open notepada first, to see results """
    session.console.keyboard.put_keys("Q: \'You want control?\'\nA: \'Yes, but just a tad...\'\n")


def CopyFile():
    """ NOT WORKING YET """
    """ Try Shared folder or Whatever to transfer between computers on one network :) """
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
    #session.close()
    session.unlock_machine()
    

def delete_last_snapshot(machine_name):
    """ WORKING """
    """ Keeps 2 last snapshots and first 'root snapshot' """
    machine = vbox.find_machine(machine_name)
    base_snapshot=machine.find_snapshot("")
    #print(base_snapshot.name)
    first_snap=list()
    last_snap=str()
    idcount=0

    while True:
        children=base_snapshot.children
        for ch in children:
            child_snap=machine.find_snapshot(ch.id_p)
            #print(ch.id_p, ch.name)
        #print(child_snap.children_count)
        if idcount==0:
            first_snap=child_snap.id_p, child_snap.name
            #print(first_snap)
            idcount+=1
        last_snap=child_snap.id_p
        #print("last:"+last_snap)
        if child_snap.children_count==0:
            break
        base_snapshot=child_snap

        if first_snap[0] != last_snap:
            #first lock session
            session=machine.create_session()
            process=session.machine.delete_snapshot(first_snap[0])
            process.wait_for_completion(timeout=-1)
            print("Deleted snapshot :"+first_snap[0])


def keep_just_base_snap(machine_name):
    """ WORKING """
    """ Delete all snapshots and keeps base one(first created snapshot) """
    machine = vbox.find_machine(machine_name)
    base_snapshot=machine.find_snapshot("")
    print(base_snapshot.name)
    snaps=[]
    #snaps=list()
    try:
        while True:
            children=base_snapshot.children
            for ch in children:
                child_snap=machine.find_snapshot(ch.id_p)
                snaps.append(child_snap.id_p)
                print(child_snap.name)
                print(child_snap.children_count)

            if child_snap.children_count==0:
                """ end deleting snapshots (no more childrens under base snapshot) """
                break
            
            base_snapshot=child_snap

        print("snaps: "+str(snaps))
        session=machine.create_session()
        for snap in snaps:
            #print(snap)
            process=session.machine.delete_snapshot(snap)
            process.wait_for_completion(timeout=-1)
            print("Deleted snapshot :"+snap)
    except:
        print("No more children snapshots.")
    #session.close()


def executecmd(machine_name):
    """ WORKING using VBoxManager.exe """
    vmname = machine_name
    command_to_run = 'services.msc' # start service (there will be Client app ?)
    username = "test"
    password = "test"
    #command = f'D:\\VirtualBox\\VBoxManage.exe guestcontrol {vmname} run --exe "cmd.exe" --username "{username}" --password "{password}" "{command_to_execute}"'
    #command = f'"D:\\VirtualBox\\VBoxManage.exe guestcontrol {vmname} run --exe "cmd.exe" --username "{username}" --password "{password}" -- {command_to_run}'
    command = f'D:\\VirtualBox\\VBoxManage.exe guestcontrol {vmname} run --exe "cmd.exe" --username "{username}" --password "{password}" -- cmd /c "{command_to_run}"'
    subprocess.Popen(command, shell=True)
    #subprocess.run(command, shell=True)
    #Popen  --> dont wait for return from command 
    #run    --> wait for return from command

def RunApp(machine_name):
    vmname = machine_name
    app_name = "notepad.exe"
    username = "test"
    password = "test"
    vboxmanage_path = r"D:\VirtualBox\VBoxManage.exe" # or add VBoxManage.exe to PATH on Computer to execute just alias

    # Check if the application is running
    command = f'"{vboxmanage_path}" guestcontrol {vmname} run --exe "cmd.exe" --username {username} --password {password} --wait-stdout -- cmd /c "tasklist' # /FI IMAGENAME eq {app_name}"
    output = subprocess.check_output(command, shell=True)
    print(output)
    if app_name not in str(output):
        print("APP{app_name}is not running....starting")
        # If the application is not running, start it
        command = f'"{vboxmanage_path}" guestcontrol {vmname} run --exe "cmd.exe" --username {username} --password {password} -- cmd /c "start {app_name}"'
        subprocess.Popen(command, shell=True)
    else:
        print("APP{app_name}is already running")
    
def CloseAllSessions(machine_name):
    """ NOT Working """
    vb = virtualbox.VirtualBox()
    machine = vb.find_machine(machine_name)
    for ses in machine.session_state:
        print(f"Session ID: {ses.id}")
        print(f"State: {ses.state}")
        print(f"Type: {ses.type}")
        print(f"User: {ses.user}")
        print("------------------")

def testcopy(machine_name,username="test",password="test"):
    """ WORKING but used with normal cmd command + VBoxManage.exe """
    """ Maybe set global username password which will be send in startup and remembered ? """
    vmname = machine_name
    filename_on_host = "D:\\01programingandtools\\PyVbox\\requirements.txt"
    directory_on_guest = "C:\\Users\\test\\Documents"
    username = username
    password = password

    command = f'D:\\VirtualBox\\VBoxManage.exe guestcontrol {vmname} copyto "{filename_on_host}" --target-directory "{directory_on_guest}" --username "{username}" --password "{password}"'

    subprocess.run(command, shell=True)


machines=listmachines()

#launchMachine("Windows10")
#Write()
#read_snapshot("Windows10","snaptest1")
#take_snapshot("Windows10","Snap_Name_TESTING")
#DownMachine()
#delete_last_snapshot("Windows10")
#keep_just_base_snap("Windows10")
#executecmd("Windows10")

#Write("testingPyVbox")
#launchMachine("testingPyVbox")
#executecmd("testingPyVbox")
#testcopy("testingPyVbox")
#RunApp("testingPyVbox")
#CloseAllSessions("testingPyVbox")
#CopyFile()
take_snapshot("testingPyVbox","Snap_Name_TESTING")

#print(virtualbox.Session().state)
#print(virtualbox.Session())

"""
TO DO :

Close All sessions after they are not needed !!! This program keeps it opened with 
Error Statement yet !! 
NOT GOOD I guess
So Close it !

"""