import os
import pyvbox

# Define the path to the file you want to copy to the virtual machine
file_path = 'D:/01programingandtools/requirements.txt'

# Define the name of the virtual machine you want to copy the file to
vm_name = 'testingPyVbox'

# Connect to VirtualBox
vbox = pyvbox.VirtualBox()

# Find the virtual machine by name
vm = vbox.find_machine(vm_name)

# Start the virtual machine
session = vm.create_session()
progress = session.machine.launch_vm_process(session, 'gui', [])
progress.wait_for_completion(-1)
#session.console.power_up() #does it work ? --> i used launch instance more in ... vm-com.py

# Get the guest session
guest_session = session.console.guest.create_session('test', '')

# Define the path to the file in the guest
guest_file_path = 'C:\\Temp\\{}'.format(os.path.basename(file_path))

# Copy the file to the guest
guest_session.file_copy_to_guest(file_path, guest_file_path)

# Close the guest session
guest_session.close()

# Shut down the virtual machine
#session.console.power_down()

# Close the session
session.close()