import subprocess
from datetime import datetime

import os

from framework.FwComponentGadget import FwComponentGadget


class StorageAccess(FwComponentGadget):
    """This allows for creation of mini file systems that can be used for storing locally or via the bus
    If this is closed early it will fuck up pretty bad and will require a restart of the device

    Args:
        readable_size:  Input the size of the file system intended e.g 4M or 512K
        filesystem:     For new filesystems this will be the format to create with e.g fat, msdos
                        For old filesystems this will be the name of the .img file e.g payloadfs.img, memes.dd
        old_fs:         Boolean value to dictate wither the class is to create a new filesystem
        debug:          Boolean value for the state of Debug prints

    functions:
        alot:           Ill get back to this

    Returns:
        tbd

    Raises:
        tbd
    """
    # Command that needs to be run for a list of available filesystems
    # compgen -c | grep "mkfs\." # Lists all file systems

    def __init__(self, readable_size, filesystem="fat", old_fs=False, debug=False):
        super().__init__(debug=debug, enabled=False)

        # Variable init for the use of an old fs
        self.old_fs = old_fs

        # There might be an alternative I'll look into
        self.readable_size = readable_size

        # Variable init for local mounting directory
        self.directory = None

        if not old_fs:
            # Create device to store to
            self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')

            # Makes a file system.
            # These don't have output of note (I should look for the error messages and check the Pi is ok with this)
            subprocess.run(["fallocate", "-l", self.readable_size, self.file_name])

            # Format file system to FAT ... for now
            subprocess.run(["mkfs."+filesystem.lower(), self.file_name])
        else:
            self.file_name = filesystem
            try:  # Check the file exists
            except: super().debug("No file that user specified.\nAttempting graceful fail")

        # To find the first available loop back device and claim it
        self.loopback_device = subprocess.run(["losetup", "-f"],stdout=subprocess.PIPE).stdout.decode('utf-8')
        if debug: print("Temp")  # Debug out what device is intended of use

        self.local_mount = False
        self.bus_mounted = False
        return

    def __del__(self):
        # No matter what call unmount?
        self.umount()
        # Then unmount from loopback
        # There is not a circumstance where it would be a good idea to allow the user to do this via umount
        return

    # This code is derived from code from dive into python. Thanks Mark <3
    def convertsize(self):
        # Copyright (c) 2009, Mark Pilgrim, All rights reserved.
        suffixes = {1024: ['K', 'M', 'G', 'T']}
        multiple = 1024
        fs_size = int(os.path.getsize(self.directory+self.file_name))
        for suffix in suffixes[multiple]:
            fs_size /= multiple
            if fs_size < multiple:
                return '{0:.1f} {1}'.format(fs_size, suffix)
        raise ValueError('Filesystem out of bounds')

    def __sizeof__(self):
        if self.old_fs:
            self.convertsize() # size of old fs

        return self.readable_size  # size of current file system

    def mountlocal(self, directory, read_only=False):
        # Mount the file system locally for amending
        # The commands are needed for this
        self.directory = directory

        # When the user tries to mount us on a non existent directory
        if not os.path.exists(self.directory):
            super().debug("No file system exists at "+directory+"\nCreating folder")
            os.mkdir("fs")
            self.directory = "./fs/"

        if read_only: subprocess.run(["mount", "-o", "ro", "/dev/"+self.loopback_device, self.directory])  # mount RO
        else: subprocess.run(["mount", "/dev/"+self.loopback_device, self.directory])  # mount norm
        return
    '''
    def mountbus(self, _write_block):
        # Mount over USB
        #If write block is possible
        if _write_block:  # mount RO
        else:  # mount norm
            return
    '''
    def unmountlocal(self):
        subprocess.run(["umount", self.directory])  # un-mount
        if self.directory == "./fs/":
            os.removedirs("fs")
        self.local_mount = False
        return
    '''
    def unmountbus(self):
        self.bus_mounted = False
        return
    
    def unmount(self):
        """
        Void function that will unmount from whatever the class is currently mounted to
        """
        if not self.local_mount:
            if not self.bus_mounted:
                return
            else:
                self.umountbus()
        else:
            self.umountlocal()
        return
    '''
