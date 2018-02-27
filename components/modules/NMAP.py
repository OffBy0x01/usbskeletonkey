import subprocess
import datetime
from components.helpers.nmap import *


class NMAP:
    """ Class for NMAP (Part of Enumeration)

             Args:
                target_is_a_file           Flag to determine if the user has requested to use a file of
                                           IP address(es) for the scanning.

                ip_file                    The file that NMAP will read to determine what IP address(es)
                                           will be scanned.

                ip                         IP address(es) that NMAP will scan.

                service_verbosity_level    Flag for the verbosity of NMAP's service detection (1-9).

                speed                      Flag for the "speed" level of the NMAP scan (T0 - T5).

                save_to_file               Boolean flag to determine if the raw output of the NMAP scan
                                           should be saved to a file.

                file_name                  The piping and filename for the optional file that the output of the
                                           NMAP scan can be saved to.

                command                    The list where the nmap command is built into.

            functions:
                check_if_file   Adds the required NMAP commands to use either targets from a file or targets
                                in the command itself

                nmap_loud       Constructs and runs the NMAP command required for a "loud" scan

                nmap_quiet      Constructs and runs the NMAP command required for a "quiet" scan

            Returns:
                ??

            Raises:
                import subprocess
        """

    # Constructor
    def __init__(self):
        self.target_is_a_file = False
        self.ip_file = "targets.txt"
        self.ip = "127.0.0.1"
        self.service_verbosity_level = "9"
        self.speed = "-T4"
        self.save_to_file = True
        self.file_name = " > temp.txt"
        self.nm = nmap.PortScanner()
        self.command = ["nmap"]

    def check_if_file(self):
        if self.target_is_a_file:  # If a file of targets is being used
            self.command = self.command + ["-iL", self.ip_file]  # Add the IP address(es) from the file to the command

        else:
            self.command = self.command + [self.ip]  # Add the IP address(es) to the command

        return

    #  "Loud scan"
    def nmap_loud(self):

        self.command = ["nmap"]  # Reset the command list
        self.check_if_file()  # Check if a file containing targets should be used

        #  Change "noise/speed" levels for the scan
        self.service_verbosity_level = "9"
        self.speed = "-T4"

        self.command = self.command + ["-sV", "--version-intensity", self.service_verbosity_level,
                                       self.speed, "-O"]  # Build command

        # Add the "save output to file" flag to the command if required
        if self.save_to_file:
            now = datetime.datetime.now()
            self.file_name = " > NMAP Loud " + str(now.strftime("%d-%m-%Y %H:%M")) + ".txt"
            self.command.append(self.file_name)

        print(self.command)  # debug
        return subprocess.run(self.command, stdout=subprocess.PIPE).stdout.decode\
            ("utf-8")  # Run command, print output to screen and return

    #  "Quiet scan"
    def nmap_quiet(self):

        self.command = ["nmap"]  # Reset the command list
        self.check_if_file()  # Check if a file containing targets should be used

        #  Change "noise/speed" levels for the scan
        self.service_verbosity_level = "1"
        self.speed = "-T2"
        self.command = self.command + ["-sV", "--version-intensity", self.service_verbosity_level, self.speed, "-O",
                                       "-D"]  # Build command

        # Add the "save output to file" flag to the command if required
        if self.save_to_file:
            now = datetime.datetime.now()
            self.file_name = " > NMAP Quiet " + str(now.strftime("%d-%m-%Y %H:%M")) + ".txt"
            self.command.append(self.file_name)

        print(self.command)  # debug
        return subprocess.run(self.command, stdout=subprocess.PIPE).stdout.decode\
            ("utf-8")  # Run command, print output to screen and return

    def os_detection(self):

        self.nm.scan(hosts=self.ip, arguments='-O')
        print(self.nm.command_line())

