import subprocess
import os

from framework.FwComponentGadget import FwComponentGadget
from datetime import datetime


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

    def createfs(self):
        super().debug("Creating a filesystem")

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')
        super().debug("Naming file system "+self.file_name)

        # Makes a file system.
        # These don't have output of note (I should look for error messages when you try to do stupid shit)
        subprocess.run(["fallocate", "-l", self.readable_size, self.file_name])  # This command accepts 1M and such
        super().debug("Running command - 'fallocate -l "+self.readable_size+" "+self.file_name+"'")

        # Format file system to FAT ... for now
        subprocess.run(["mkfs."+self.fs.lower(), self.file_name])
        super().debug("Running command - 'mkfs."+self.fs.lower()+" "+self.file_name+"'")

    def __init__(self, readable_size, fs="fat", old_fs=False, debug=False):
        # Starting the super class first
        super().__init__(debug=debug, enabled=False)  # TODO

        # Inform the user on debug what module has started
        super().debug("Starting Module: Storage Access")

        # Variable init
        self.fs = fs
        self.old_fs = old_fs
        self.readable_size = readable_size
        self.directory = None

        if not old_fs:
            self.createfs()
        else:
            super().debug("Attempting to use existing filesystem")

            self.file_name = fs
            super().debug("User specified file to load as " + fs)

            if not os.path.isfile(self.file_name):  # Check the file exists
                self.createfs()
                super().debug("File that user specified does not exist.\nWill Create a new filesystem.")

        # To find the first available loop back device and claim it
        self.loopback_device = subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8')

        subprocess.run()
        super().debug("Attempting to mount on "+self.loopback_device)

        # If the first loopback device available is still the one we should be mounted to
        if self.loopback_device == subprocess.run(["losetup", "-f"], stdout=subprocess.PIPE).stdout.decode('utf-8'):
            super().debug("Something went wrong here. Insufficient permissions?")
            # TODO Insert method of graceful fail here

        self.local_mount = False
        self.bus_mounted = False
        return

    def __del__(self):
        # No matter what call unmount?
        self.umount()
        # Then unmount from loopback

        # There is not a circumstance where it would be a good idea to allow the user to do this via umount so only on
        # __del__ should it be called to remove from loopback
        return

    # This code is derived from code from dive into python. Thanks Mark <3
    def convertsize(self):
        # Copyright (c) 2009, Mark Pilgrim, All rights reserved.

        # This should never reach T unless the Pi is using external storage or we are in the year 2100
        suffixes = {1024: ['K', 'M', 'G', 'T']}
        multiple = 1024
        fs_size = int(os.path.getsize(self.directory+self.file_name))
        for suffix in suffixes[multiple]:
            fs_size /= multiple
            if fs_size < multiple:
                return '{0:.1f} {1}'.format(fs_size, suffix)
        raise ValueError('Filesystem out of bounds (this is an easy fix if necessary)')

    def __sizeof__(self):
        if self.old_fs:
            self.convertsize()  # size of old fs

        return self.readable_size  # size of current file system

    def mountlocal(self, directory="./fs/", read_only=False):
        # Mount the file system locally for amending
        # The commands are needed for this
        self.directory = directory

        # When the user tries to mount us on a non existent directory
        if not os.path.exists(self.directory):
            super().debug("No file system exists at "+directory+"\nCreating folder")
            os.mkdir("fs")
            self.directory = "./fs/"

        if read_only:
            subprocess.run(["mount", "-o", "ro", "/dev/"+self.loopback_device, self.directory])  # mount RO
        else:
            subprocess.run(["mount", "/dev/"+self.loopback_device, self.directory])  # mount norm
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
