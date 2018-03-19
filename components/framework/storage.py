import os
import subprocess
from datetime import datetime

from components.framework.FwComponentGadget import FwComponentGadget


class StorageAccess(FwComponentGadget):
    """This allows for creation of mini file systems that can be used for storing locally or via the bus
    If this is closed early it will fuck up pretty bad and will require a restart of the device

    Args:
        readable_size:  Input the size of the file system intended
                            e.g 4M, 512K. This defaults to 2M
        fs:             For new filesystems this will be the format to create with
                            e.g fat, msdos
                        For old filesystems this will be the name of the .img file
                            e.g payloads.img, memes.dd
        old_fs:         Boolean value to dictate wither the class is to create a new filesystem
        directory:      String dictating the file system will exist within
                            e.g "./", "/mnt/", "../fs/"
        debug:          Boolean value for the state of Debug prints

    functions:
        alot:           Ill get back to this

    Returns:
        tbd

    Raises:
        tbd


    TODO:
        Add functionality to copy specific files from SkelKey to the target via OTG

        Put disclaimers on scary bits of code

    """
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

    def __createfs(self):
        """
        Creates a file system: This action does not require sudo. This action does not have exit codes
        """
        self.debug("    Creating a filesystem")

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')
        self.debug("    Naming file system " + self.file_name)

        # Makes a file system. (This command accepts 1M and such)
        # These don't have output of note (I should look for error messages when you try to do stupid shit)
        subprocess.run(["fallocate", "-l", self.readable_size, self.directory + self.file_name])
        self.debug("    Running command - 'fallocate -l " + self.readable_size
                      + " " + self.directory + self.file_name + "'")

        # Format file system to FAT ... for now
        subprocess.run(["mkfs." + self.fs.lower(), self.directory + self.file_name])
        self.debug("    Running command - 'mkfs." + self.fs.lower() + " " + self.directory + self.file_name + "'")
        # Done

    def __init__(self, readable_size="2M", fs="fat", old_fs=False, directory="./", debug=False):
        # Initialise super class
        super().__init__("g_mass_storage", enabled=False, debug=debug)
        self._type = "Component"
        self._name = "Storage"

        # Inform the user on debug what module has started
        self.debug("Starting Module: Storage Access")

        # Variable init
        self.fs = fs
        self.old_fs = old_fs
        self.directory = directory
        self.mounted_dir = str(None)
        self.loopback_device = str(None)
        self.readable_size = readable_size

        if not old_fs:
            self.__createfs()
        else:
            self.debug("Attempting to use existing filesystem")

            self.file_name = fs
            self.debug("User specified to load " + fs)

            # If file exists
            if os.path.isfile(self.file_name):
                self.debug("File discovered")
            else:
                self.debug("File" + self.file_name + "does not exist: 2.04")
                exit(2.04)

        self.local_mount = False
        self.bus_mounted = False
        return

    def __del__(self):
        # TODO move the auto mount that I had here into exit
        self.debug("Removed")
        return

    # This code is derived from code from dive into python. Thanks Mark <3
    def convertsize(self):
        # Copyright (c) 2009, Mark Pilgrim, All rights reserved.

        # This should never reach T unless the Pi is using external storage or we are in the year 2100
        suffixes = {1024: ['K', 'M', 'G', 'T']}
        multiple = 1024
        fs_size = int(os.path.getsize(self.directory + self.file_name))
        for suffix in suffixes[multiple]:
            fs_size /= multiple
            if fs_size < multiple:
                return '{0:.1f} {1}'.format(fs_size, suffix)
        raise ValueError('Filesystem out of bounds (Why is it over 1023 TB?!)')

    # Overwriting the default sizeof method
    def __sizeof__(self):
        if self.old_fs:
            self.convertsize()  # size of old fs

        return self.readable_size  # size of current file system

    def mountlocal(self, directory="./fs/", read_only=False):  # make this more unique for a default folder
        # Mount the file system locally for amending of any desc (unless RO)

        self.loopback_device = subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        mount_loopback = ["losetup"]

        if read_only:
            mount_loopback = mount_loopback + ["-r"]

        mount_loopback = mount_loopback + [self.loopback_device, (self.directory + self.file_name)]

        self.debug("Attempting to mount on " + self.loopback_device)

        loop_output = subprocess.run(mount_loopback, stdout=subprocess.PIPE).stdout.decode('utf-8')

        if "failed to set up loop device" in loop_output:
            self.debug("Error mounting on loop back " + self.loopback_device + ": 2.04")
            exit(2.04)

        # If the first loop back device available is still the one we should be mounted to
        if self.loopback_device == subprocess.run(["losetup", "-f"],
                                                  stdout=subprocess.PIPE).stdout.decode('utf-8'):
            self.debug("Loop back setup Failed: 2.04")
            exit(2.04)

        # The directory we intend to mount to
        self.mounted_dir = directory

        # When the user tries to mount us on a non existent directory
        if not os.path.exists(self.mounted_dir):
            self.debug("Directory Traversal failure: No directory at " + directory + "\nCreating folder")
            os.mkdir(self.mounted_dir)

        if read_only:
            mount_command = ["mount", "-o", "ro", self.loopback_device, self.mounted_dir]  # mount RO
        else:
            mount_command = ["mount", self.loopback_device, self.mounted_dir]  # mount norm

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
        self.debug("Mounted over bus. RO: " + write_block.__str__())
        self.bus_mounted = True
        return

    def unmountlocal(self):
        self.debug(subprocess.run(["umount", self.mounted_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))  # un-mount
        self.debug("The filesystem was unmounted with command umount " + self.mounted_dir)

        self.debug("Now removing from loopback device with command - losetup -d " + self.loopback_device)
        subprocess.run(["losetup", "-d", self.loopback_device])

        self.local_mount = False
        self.loopback_device = str(None)
        self.mounted_dir = str(None)
        return

    def unmountbus(self):
        self.disable()

        self.debug("The bus was unmounted")
        self.bus_mounted = False
        return

    def unmount(self):
        self.debug("Starting unmount")

        if self.local_mount:
            self.debug("Filesystem is mounted on " + self.mounted_dir)
            self.unmountlocal()
            return

        if self.bus_mounted:
            self.debug("Filesystem is mounted on the bus")
            self.unmountbus()
            return

        self.debug("Nothing was mounted")
        return
