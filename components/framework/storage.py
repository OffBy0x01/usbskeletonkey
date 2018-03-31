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
                :param fs: This is used to mount a old file system. Fill this with a string of the name of the file
                             system you wish to mount
                :param directory: Directory of where the filesystem should work from. Either path to Filesystem or
                                    where filesystem will rest. Defaults to "./"
                :param debug: Whether to enable debug output for this module. This is passed to the superclass.
                                Defaults to False

            Functions:
                __init__: The class initialisation uses the above parameters to open the appropriate file system
                __createfs: Hidden method that is called as and when relevant by the __init__ function
                __del__: Called when the Class is closed simply pushes a debug that it has been closed
                __convertsize: Hidden method used to convert the size of a file to a string ending in the
                                appropriate suffix
                __sizeof__: Returns the size of the current file system after running through convert where appropriate
                mountlocal: Mounts the file system locally to the set directory
                mountbus: Mounts the file system on the bus
                unmountlocal: unmounts locally where applicable
                unmountbus: unmounts the bus where applicable
                unmount: Calls the appropriate unmount file system if mounted
    """

    def __createfs(self):
        """
        Creates a file system: This action does not require sudo. This action does not have exit codes
        """
        self.storage.debug("    Creating a filesystem")

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')
        self.storage.debug("    Naming file system " + self.file_name)

        # Makes a file system. (This command accepts 1M and such)
        falloc = ["fallocate", "-l", self.readable_size.upper(), self.directory + self.file_name]
        self.storage.debug("    Running command - " + falloc.__str__())
        subprocess.run(falloc)

        # Make a file system
        mklabel = ["parted", self.directory + self.file_name, "mklabel", "msdos"]
        self.storage.debug("    Running command - " + mklabel.__str__())
        subprocess.run(mklabel)

        mkpart = ["parted", self.directory + self.file_name, "mkpart", "primary", self.fs.lower(), "0%", "100%", "ignore"]
        self.storage.debug("    Running command - " + mkpart.__str__())
        subprocess.run(mkpart)

        loopback_temp = self.__loopmount(False)

        mkfs = ["mkfs." + self.fs[:3], loopback_temp + "p1"]
        self.storage.debug("    Running command - " + mkfs.__str__())
        subprocess.run(mkfs)

        subprocess.run(["losetup", "-d", loopback_temp])

        # Done

    def __init__(self, readable_size="4M", fs=None, directory="./", debug=False):
        # Initialise super class
        super().__init__("g_mass_storage", enabled=False, debug=debug)
        self._type = "Component"
        self._name = "Storage"

        # Start debuger
        self.storage = Debug(debug=debug)

        # Inform the user on debug what module has started
        self.storage.debug("Starting Module: Storage Access")

        # Variable init
        if fs is None:
            self.fs = "fat32"
        else:
            self.fs = fs

        self.old_fs = fs is None
        self.directory = directory
        self.mounted_dir = str(None)
        self.loopback_device = str(None)
        self.readable_size = readable_size

        if fs is None:
            self.__createfs()
        else:
            self.storage.debug("Attempting to use existing filesystem")

            self.file_name = fs
            self.storage.debug("User specified to load " + fs)

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

    def __convertsize(self):
        # This code is derived from code from dive into python. Thanks Mark <3

        # This should never reach T unless the Pi is using external storage or we are in the year 2100
        suffixes = {1024: ['K', 'M', 'G', 'T']}
        multiple = 1024
        fs_size = int(os.path.getsize(self.directory + self.file_name))
        for suffix in suffixes[multiple]:
            fs_size /= multiple
            if fs_size < multiple:
                return '{0:.1f} {1}'.format(fs_size, suffix)
        raise ValueError('Filesystem out of bounds (Why is it over 1023 TB?!)')
        # Copyright (c) 2009, Mark Pilgrim, All rights reserved.

    # Overwriting the default sizeof method
    def __sizeof__(self):
        if self.old_fs:
            self.__convertsize()  # size of old fs

        return self.readable_size  # size of current file system

    def __loopmount(self, read_only):
        loopback_device = subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        mount_loopback = ["losetup", "-P"]

        if read_only:
            mount_loopback = mount_loopback + ["-r"]

        mount_loopback = mount_loopback + [loopback_device, (self.directory + self.file_name)]

        self.storage.debug("Attempting to mount on " + loopback_device)

        loop_output = subprocess.run(mount_loopback, stdout=subprocess.PIPE).stdout.decode('utf-8')

        if "failed to set up loop device" in loop_output:
            self.storage.debug("Error mounting on loop back " + loopback_device + ": 2.04")
            exit(2.04)

        # If the first loop back device available is still the one we should be mounted to
        if loopback_device == subprocess.run(["losetup", "-f"],
                                                  stdout=subprocess.PIPE).stdout.decode('utf-8'):
            self.storage.debug("Loop back setup Failed: 2.04")
            exit(2.04)

        return loopback_device

    def mountlocal(self, directory="./fs/", read_only=False):  # make this more unique for a default folder
        # Mount the file system locally for amending of any desc (unless RO)

        # Mount on LO device
        self.loopback_device = self.__loopmount(read_only)

        # The directory we intend to mount to
        self.mounted_dir = directory

        # When the user tries to mount us on a non existent directory
        if not os.path.exists(self.mounted_dir):
            self.storage.debug("Directory Traversal failure: No directory at " + directory + "\nCreating folder")
            os.mkdir(self.mounted_dir)

        if read_only:
            mount_command = ["mount", "-o", "ro", self.loopback_device + "p1", self.mounted_dir]  # mount RO
        else:
            mount_command = ["mount", self.loopback_device + "p1", self.mounted_dir]  # mount norm

        subprocess.run(mount_command)

        self.local_mount = True
        return

    def mountbus(self, write_block=False):
        # Mount over USB
        if write_block:
            # modprobe g_mass_storage ro=1 file=./foo.bar
            self.vendor_id = "ro=1"  # This only accepts y or 1 for true
            self.product_id = "file=" + self.directory + self.file_name
        else:
            # modprobe g_mass_storage ro=0 file=./foo.bar
            self.vendor_id = "ro=0"
            self.product_id = "file=" + self.directory + self.file_name

        self.enable()
        self.storage.debug("Mounted over bus. RO: " + write_block.__str__())
        self.bus_mounted = True
        return

    def unmountlocal(self):
        self.storage.debug(subprocess.run(["umount", self.mounted_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))  # un-mount
        self.storage.debug("The filesystem was unmounted with command umount " + self.mounted_dir)

        self.storage.debug("Now removing from loopback device with command - losetup -d " + self.loopback_device)
        subprocess.run(["losetup", "-d", self.loopback_device])

        self.local_mount = False
        self.loopback_device = str(None)
        self.mounted_dir = str(None)
        return

    def unmountbus(self):
        self.disable()

        self.storage.debug("The bus was unmounted")
        self.bus_mounted = False
        return

    def unmount(self):
        self.storage.debug("Starting unmount")

        if self.local_mount:
            self.storage.debug("Filesystem is mounted on " + self.mounted_dir)
            self.unmountlocal()
            return

        if self.bus_mounted:
            self.storage.debug("Filesystem is mounted on the bus")
            self.unmountbus()
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
