import os
import subprocess
from datetime import datetime

from components.framework.FwComponentGadget import FwComponentGadget
from components.framework.Debug import *


class StorageAccess(FwComponentGadget):
    """
    This allows for creation of mini file systems that can be used for storing locally or via the bus
    If this is closed early it will fuck up pretty bad and should require a restart of the device
            Super Class: FwComponentGadget

            __init__ asks for:
                :param readable_size: This will set the Size of a NEW file system. Default is 2M
                :param file_name: This is used to mount a old file system. Fill this with a string of the name of the
                                    file system you wish to mount
                :param file_path: Directory of where the filesystem should work from. Either path to Filesystem or
                                    where filesystem will rest. Defaults to "./"
                :param debug: Whether to enable debug output for this module. This is passed to the superclass.
                                Defaults to False

            Functions:
                __init__: The class initialisation uses the above parameters to open the appropriate file system
                __create_fs: Hidden method that is called as and when relevant by the __init__ function
                __del__: Called when the Class is closed simply pushes a debug that it has been closed
                __convert_size: Hidden method used to convert the size of a file to a string ending in the
                                appropriate suffix
                __sizeof__: Returns the size of the current file system after running through convert where appropriate
                mount_local: Mounts the file system locally to the set file_path
                mount_bus: Mounts the file system on the bus
                unmount_local: Will unmount locally where applicable
                unmount_bus: Will unmount the bus where applicable
                unmount: Calls the appropriate unmount file system if mounted
    """

    def __create_fs(self):
        """
        Creates a file system: This action does not require sudo. This action does not have exit codes
        """
        self.storage.debug("    Creating a filesystem")

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')
        self.storage.debug("    Naming file system " + self.file_name)

        # Makes a file system. (This command accepts 1M and such)
        file_allocate = ["fallocate", "-l", self.readable_size.upper(), self.file_path + self.file_name]
        self.storage.debug("    Running command - " + file_allocate.__str__())
        subprocess.run(file_allocate)

        # Make a file system
        make_label = ["parted", "--script", self.file_path + self.file_name, "mklabel", "msdos"]
        self.storage.debug("    Running command - " + make_label.__str__())
        subprocess.run(make_label)

        make_partition = ["parted", "--script",
                          self.file_path + self.file_name, "mkpart", "primary", "fat32", "0%", "100%"]

        self.storage.debug("    Running command - " + make_partition.__str__())
        subprocess.run(make_partition)

        loop_back_temp = self.__loop_mount(False)

        make_file_system = ["mkfs.fat", loop_back_temp + "p1"]
        self.storage.debug("    Running command - " + make_file_system.__str__())
        subprocess.run(make_file_system)

        subprocess.run(["losetup", "-d", loop_back_temp])

        # Done

    def __init__(self, readable_size="4M", file_name=None, file_path="./", debug=False):
        # Initialise super class
        super().__init__("g_mass_storage", enabled=False, debug=debug)
        self._type = "Component"
        self._name = "Storage"

        # Start debugger
        self.storage = Debug(debug=debug)

        # Inform the user on debug what module has started
        self.storage.debug("Starting Module: Storage Access")

        # Variable init
        self.old_fs = (file_name is None)
        self.file_path = file_path
        self.mounted_dir = str(None)
        self.loop_back_device = str(None)
        self.readable_size = readable_size

        if file_name is None:
            self.__create_fs()
        else:
            self.storage.debug("Attempting to use existing filesystem")

            self.file_name = file_name
            self.storage.debug("User specified to load " + file_name)

            # If file exists
            if os.path.isfile(self.file_name):
                self.storage.debug("File discovered")
            else:
                self.storage.debug("File" + self.file_name + "does not exist: 2.04")
                exit(2.04)

        self.local_mount = False
        self.bus_mounted = False
        return

    def __del__(self):
        self.storage.debug("Removed")
        return

    def __convert_size(self):
        # This code is derived from code from dive into python. Thanks Mark <3

        # This should never reach T unless the Pi is using external storage or we are in the year 2100
        suffixes = {1024: ['K', 'M', 'G', 'T']}
        multiple = 1024
        fs_size = int(os.path.getsize(self.file_path + self.file_name))
        for suffix in suffixes[multiple]:
            fs_size /= multiple
            if fs_size < multiple:
                return '{0:.1f} {1}'.format(fs_size, suffix)
        raise ValueError('Filesystem out of bounds (Why is it over 1023 TB?!)')
        # Copyright (c) 2009, Mark Pilgrim, All rights reserved.

    # Overwriting the default sizeof method
    def __sizeof__(self):
        if self.old_fs:
            self.__convert_size()  # size of old fs

        return self.readable_size  # size of current file system

    def __loop_mount(self, read_only):
        loop_back_device = subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        mount_loop_back = ["losetup", "-P"]  # -P checks for partitions

        if read_only:
            mount_loop_back += ["-r"]

        mount_loop_back += [loop_back_device, (self.file_path + self.file_name)]

        self.storage.debug("Attempting to mount on " + loop_back_device)
        loop_output = subprocess.run(mount_loop_back, stdout=subprocess.PIPE).stdout.decode('utf-8')

        if "failed to set up loop device" in loop_output:
            self.storage.debug("Error mounting on loop back " + loop_back_device + ": 2.04")
            exit(2.04)

        # If the first loop back device available is still the one we should be mounted to
        if loop_back_device == subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8'):
            self.storage.debug("Loop back setup Failed: 2.04")
            exit(2.04)

        return loop_back_device

    def mount_local(self, directory="./fs/", read_only=False):  # make this more unique for a default folder
        # Mount the file system locally for amending of any desc (unless RO)
        mount_command = ["mount"]
        # Mount on LO device
        self.loop_back_device = self.__loop_mount(read_only)

        # The file_path we intend to mount to
        self.mounted_dir = directory

        # When the user tries to mount us on a non existent file_path
        if not os.path.exists(self.mounted_dir):
            self.storage.debug("Directory Traversal failure: No file_path at " + directory + "\nCreating folder")
            os.mkdir(self.mounted_dir)

        if read_only:
            mount_command += ["-o", "ro", self.loop_back_device + "p1", self.mounted_dir]  # mount RO
        else:
            mount_command += [self.loop_back_device + "p1", self.mounted_dir]  # mount norm

        subprocess.run(mount_command)

        self.local_mount = True
        return

    def mount_bus(self, write_block=False):
        # Mount over USB
        if write_block:
            # modprobe g_mass_storage ro=1 file=./foo.bar
            self.vendor_id = "ro=1"  # This only accepts y or 1 for true
            self.product_id = "file=" + self.file_path + self.file_name
        else:
            # modprobe g_mass_storage ro=0 file=./foo.bar
            self.vendor_id = "ro=0"  # Read Only = 0
            self.product_id = "file=" + self.file_path + self.file_name

        self.enable()
        self.storage.debug("Mounted over bus. RO: " + write_block.__str__())
        self.bus_mounted = True
        return

    def unmount_local(self):
        unmount = ["umount", self.mounted_dir]
        self.storage.debug(subprocess.run(unmount, stdout=subprocess.PIPE).stdout.decode('utf-8'))
        self.storage.debug("The filesystem was unmounted with command - " + unmount.__str__())

        del_loop_device = ["losetup", "-d", self.loop_back_device]
        subprocess.run(del_loop_device)
        self.storage.debug("Loop back device removed with command - " + del_loop_device.__str__())

        self.local_mount = False
        self.loop_back_device = str(None)
        self.mounted_dir = str(None)
        return

    def unmount_bus(self):
        self.disable()

        self.storage.debug("The bus was unmounted")
        self.bus_mounted = False
        return

    def unmount(self):
        self.storage.debug("Starting unmount")

        if self.local_mount:
            self.storage.debug("Filesystem is mounted on " + self.mounted_dir)
            self.unmount_local()
            return

        if self.bus_mounted:
            self.storage.debug("Filesystem is mounted on the bus")
            self.unmount_bus()
            return

        self.storage.debug("Nothing was mounted")
        return

    '''
    Notes:
        Found a cool thing with g_mass_storage. It is capable of mounting multiple volumes but because of the time of 
        discovery this feature will be ignored/left for now. A second version of storage could be created to bring the 
        use of this discovery but it doesn't seem worth it for now.
        Documentation -- http://www.linux-usb.org/gadget/file_storage.html

        This classes intended use was to have the possibility of multiple instances. This is now open to change via
        progression with the information above as instead of having multiple instances of storage devices that can
        be mounted we could alternatively have a stripped back class and have it called by a handler. This would allow 
        for less control from other modules directly however. This will be left open to later changes and classed as
        'Gold Plating'

        TODO I dont think the pi will be able to recognise when the file system is done with one the bus
        This could pose a serious issue in regard to ensuring the Skeleton keys ability to run corruption free
        This should be looked into further in testing
        Documentation -- http://elixir.free-electrons.com/linux/latest/source/Documentation/usb/mass-storage.txt
                         http://elixir.free-electrons.com/linux/latest/source/Documentation/usb/usbmon.txt
    '''
