
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
        self.service_verbosity_level = "9"
        self.speed = "-T4"
        self.save_output = False
        self.file_name = " > temp.txt"
        self.nm = nmap.PortScanner()
        self.loud_scan = True
        self.targets = ""

    def output(self):  # Quick "mockup" for output

        print('----------------------------------------------------')
        print('Host : %s (%s)' % (self.targets, self.nm[self.targets].hostname()))
        print('State : %s' % self.nm[self.targets].state())

        for protocol in self.nm[self.targets].all_protocols():
            print('----------')
            print('Protocol : %s' % protocol)
            print('----------')

            for port in self.nm[self.targets][protocol]:
                nmap_results = self.nm[self.targets][protocol][port]

                print('PORT: ' + str(port) + ': ' + "SERVICE: " + nmap_results['product']
                      + " VERSION: " + nmap_results['version'] + " STATE: " + nmap_results['state'])

            # TODO - Sort output for OS detection.
            # For outputting -sV info use the keys: product and version (Service running and version)
            # For outputting -O info I HAVE NO CLUE on the keys. "osclass" should work but it doesn't

    def output_to_file(self):

        # FILE OUTPUT BULLSHIT!
        return

    def service_detection(self, target, port_range, port_start, port_end):

        self.targets = target

        if self.loud_scan:
            if port_range:
                command = "-p " + port_start + "-" + port_end + " -sV --version-light -T4"
                self.nm.scan(hosts=self.targets, arguments=command)
            else:
                command = "-sV --version-all -T4"
                self.nm.scan(hosts=self.targets, arguments=command)

        else:
            if port_range:
                command = "-p " + port_start + "-" + port_end + " -sV --version-light"
                self.nm.scan(hosts=self.targets, arguments=command)
            else:
                command = "-sV --version-light"
                self.nm.scan(hosts=self.targets, arguments=command)

        print(self.nm.command_line())  # debug

        if self.save_output:
            return self.output_to_file()
        else:
            return self.output()

    def os_detection(self, target, scan_loud, save_output):

        self.targets = target
        self.loud_scan = scan_loud
        self.save_output = save_output

        if self.loud_scan:
            self.nm.scan(hosts=target, arguments="-O --osscan-guess -T5")

        else:
            self.nm.scan(hosts=target, arguments="-O")

        print(self.nm.command_line())  # debug

       # return self.service_detection()

