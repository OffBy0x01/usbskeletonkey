import subprocess
import os

from framework.FwComponentGadget import FwComponentGadget
from datetime import datetime


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
        super().debug("    Creating a filesystem")

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')
        super().debug("    Naming file system " + self.file_name)

        # Makes a file system. (This command accepts 1M and such)
        # These don't have output of note (I should look for error messages when you try to do stupid shit)
        subprocess.run(["fallocate", "-l", self.readable_size, self.directory + self.file_name])
        super().debug("    Running command - 'fallocate -l " + self.readable_size
                      + " " + self.directory + self.file_name + "'")

        # Format file system to FAT ... for now
        subprocess.run(["mkfs." + self.fs.lower(), self.directory + self.file_name])
        super().debug("    Running command - 'mkfs." + self.fs.lower() + " " + self.directory + self.file_name + "'")
        # Done

    def __init__(self, readable_size=None, fs="fat", old_fs=False, directory="./", debug=False):
        # Starting the super class first
        super().__init__("g_mass_storage", enabled=False, debug=debug)

        # Inform the user on debug what module has started
        super().debug("Starting Module: Storage Access")

        # Variable init
        self.fs = fs
        self.old_fs = old_fs
        self.directory = directory

        # In the event the user wants a default value
        if readable_size is None:
            self.readable_size = "2M"  # TODO add a default size to config?
        else:
            self.readable_size = readable_size

        if not old_fs:
            self.__createfs()
        else:
            super().debug("Attempting to use existing filesystem")

            self.file_name = fs
            super().debug("User specified to load " + fs)

            # If file exists
            if os.path.isfile(self.file_name):
                super().debug("File discovered")
            else:
                super().debug("File that user specified does not exist. "
                              "Will Create a new filesystem")
                self.__createfs()

        # To find the first available loop back device and claim it
        self.loopback_device = subprocess.run(["losetup", "-f"],
                                              stdout=subprocess.PIPE).stdout.decode('utf-8')

        if "Permission denied" in self.loopback_device:
            super().debug("Permissions are required"
                          "This should be running as root or at least some sort of admin"
                          "Now attempting to fail gracefully")
            # TODO Try to find an alternative method of storage and drop the ability to mount on bus

        super().debug("Attempting to mount on " + self.loopback_device +
                      "Running Command - losetup " + self.loopback_device + " " + self.directory + self.file_name)
        # When using 'losetup' offset should not be required in our use case as we will be using a single partition
        loop_output = subprocess.run(["losetup", self.loopback_device, self.directory + self.file_name],
                                     stdout=subprocess.PIPE).stdout.decode('utf-8')

        if "failed to set up loop device" in loop_output:
            super().debug("The file attempted to load onto the loopback device cannot be mounted\n" +
                          "Attempting to recover...")
            self.__createfs()

        # If the first loopback device available is still the one we should be mounted to
        if self.loopback_device == subprocess.run(["losetup", "-f"],
                                                  stdout=subprocess.PIPE).stdout.decode('utf-8'):
            super().debug("Something went wrong here"
                          "The next available loopback is the loopback we should be on, IDK")
            # TODO Insert method of graceful fail here

        self.local_mount = False
        self.bus_mounted = False
        return

    def __del__(self):
        super().debug("Storage class is being deleted")
        # No matter what call unmount?
        super().debug("Running unmount to ensure the file system is not being left active")
        self.unmount()

        super().debug("Now removing from loopback device with command - losetup -d " + self.loopback_device)
        subprocess.run(["losetup", "-d", self.loopback_device])
        # There is not a circumstance where it would be a good idea to allow the user to do this via umount so only on
        # __del__ should it be called to remove from loopback

        super().debug("Storage class has been successfully removed")
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
        raise ValueError('Filesystem out of bounds (this is an easy fix if necessary)')

    # Overwriting the default sizeof method
    def __sizeof__(self):
        if self.old_fs:
            self.convertsize()  # size of old fs

        return self.readable_size  # size of current file system

    def mountlocal(self, directory="./fs/", read_only=False):
        # Mount the file system locally for amending of any desc (unless RO)

        # The directory we intend to mount to
        self.directory = directory

        # When the user tries to mount us on a non existent directory
        if not os.path.exists(self.directory):
            super().debug("No file system exists at " + directory + "\nCreating folder")
            os.mkdir(self.directory)

        if read_only:
            subprocess.run(["mount", "-o", "ro", "/dev/" + self.loopback_device, self.directory])  # mount RO
        else:
            subprocess.run(["mount", "/dev/" + self.loopback_device, self.directory])  # mount norm
        return

    def mountbus(self, write_block=False):
        # Mount over USB
        #
        if write_block:
            # modprobe g_mass_storage ro=1 file=foo.bar
            super().vendor_id = "ro=1"  # This only accepts y or 1 for true
            super().product_id = "file=" + self.directory + self.file_name
            super().enable()
            super().debug("Mounted over bus (RO)")  # mount RO
        else:
            # modprobe g_mass_storage file=foo.bar
            super().vendor_id = "file=" + self.directory + self.file_name
            super().debug("Mounted over bus")  # mount norm
        self.bus_mounted = True
        return

    def unmountlocal(self):
        subprocess.run(["umount", self.directory])  # un-mount
        super().debug("The filesystem was unmounted with command umount " + self.directory)
        if self.directory == "./fs/":
            super().debug("    Default directory was used; it will now be removed")
            os.removedirs("fs")
        self.local_mount = False
        return

    def unmountbus(self):
        super().disable()
        super().debug("The bus was unmounted")
        self.bus_mounted = False
        return

    def unmount(self):
        super().debug("Starting unmount")
        if not self.local_mount:
            if not self.bus_mounted:
                super().debug("Nothing was mounted")
                return

            else:
                super().debug("Filesystem is mounted on the bus")
                self.unmountbus()
                return

        else:
            super().debug("Filesystem is mounted on " + self.directory)
            self.unmountlocal()
        return


# debugging
if __name__ == '__main__':
    bp = "\u2022"

    print("This is an example run of specifically the storage class"
          "The intent is to:\n" +
          bp + " Open a new file system\n" +
          bp + " Mount locally\n" +
          bp + " Add a file\n" +
          bp + " Close the file system\n" +
          bp + " Confirm the closure\n" +
          bp + " Reopen the file system\n" +
          bp + " Read from it\n" +
          bp + " Close it again\n"
               "This will be done with two classes in debug mode")

    print("Starting Test One")
    TestOne = StorageAccess(debug=True)

    print("Size " + TestOne.__sizeof__())

    TestOne.mountlocal()

    if not os.path.exists(TestOne.directory):
        print("TEST ONE: The file system did not make a directory correctly")
        exit(1)

    subprocess.run(["touch", TestOne.directory + "Test\ File"])
    print("Should've created a file there")

    if not os.path.isfile(TestOne.directory + "Test\ File"):
        print("Did not create a file")
        exit(1)

    test_one_file = TestOne.file_name
    test_one_directory = TestOne.directory
    print("Attributes of TestOne are saved")

    TestOne.unmount()
    del TestOne

    if os.path.exists(test_one_directory):
        if os.path.isfile("./" + test_one_directory + "/" + test_one_file):
            print("The file system did not unmount correctly")
            exit(1)

    print("Starting Test Two")
    TestTwo = StorageAccess(fs=test_one_file, old_fs=True, debug=True)

    print("Size " + TestTwo.__sizeof__())

    TestTwo.mountlocal("./TestTwo/", True)

    if not os.path.exists(TestTwo.directory):
        print("TEST TWO: The file system did not mount correctly")
        exit(1)

    if not os.path.isfile(TestTwo.directory + "Test\ File"):
        print("TEST TWO: Could not see file")
        exit(1)

    del TestTwo
    exit(0)