import virtualbox


def listMachines():
    vbox = virtualbox.VirtualBox()
    print("List of machines: ")
    print(30*"-")
    for machine in vbox.machines:
        print("\t+ ", machine.name)
    print(30*"-")

listMachines()