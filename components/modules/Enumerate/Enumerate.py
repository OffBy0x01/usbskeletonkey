import struct
import subprocess

import nmap

from components.framework.Debug import Debug
from components.helpers.IpValidator import *
from components.helpers.ModuleManager import ModuleManager


class TargetInfo:
    def __init__(self):
        self.OS_INFO = []
        self.SOFTWARE_INFO = []
        self.WORKGROUP = []
        self.DOMAIN = []  # USERS + GROUPS
        self.LOCAL = []  # USERS + GROUPS
        self.SESSIONS = []
        self.NBT_STAT = []
        self.SHARE_INFO = []  # include SMB info?
        self.PASSWD_POLICY = []
        self.PRINTER_INFO = []
        self.PORTS = {}  # prolly formatted like this "PORT_NUMBER : STATUS"

#-.-. --- .-. . -.-- .... .- ... -. --- --. --- --- -.. .. -.. . .- ...


class Enumerate(Debug):
    def __init__(self, debug=False):
        super().__init__(name="Enumerate", type="Module", debug=debug)

        self.nm = nmap.PortScanner()

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)
        if not self.current_config:
            self.debug("Error: could not import config of " + self._name)

        # ~Produce list of usable ip addresses~
        ip_targets = self.current_config.options["ip_targets"]
        ip_exclusions = self.current_config.options["ip_exclusions"]
        self.ip_list = [ip for ip in self.get_ip_list(ip_targets) if ip not in self.get_ip_list(ip_exclusions)]

        # ~Produce list of usable ports~
        ports = self.current_config.options["port_targets"]
        port_exclusions = self.current_config.options["port_exclusions"]
        self.port_list = [port for port in self.get_port_list(ports) if port not in self.get_port_list(port_exclusions)]

        # ~Produce list of usable users~
        # -- Andrew
        #
        self.user_list = "I've not implemented this yet"

        self.quiet = self.current_config.options["quiet"]
        self.verbose = self.current_config.options["verbose"]
        self.use_port_range = self.current_config.options["use_port_range"]


    # ~Runs all the things~
    # ---------------------
    def enumeration(self):
        for ip in self.ip_list:
            for port in self.port_list:
                # self.other thing that uses ports
                pass
            for user in self.user_list:
                # self.other thing that uses users
                pass

            #self.other things that just uses IPs
        # TODO PUT ALL THE THINGS IN HERE - If format doesn't work for you hmu with why



    def get_port_list(self, current):
        # TODO 01/03/18 [1/2] Add error handling
        if "," in current:
            return current.strip().split(',')
        elif "-" in current:
            start, _, end = current.strip().partition('-')
            return [port for port in range(int(start), int(end))]
        else:
            return [current]

    def get_ip_list(self, current):
        # TODO 01/03/18 [2/2] Add error handling
        # List of IPs
        if "," in current:
            return current.strip().split(',')
        # Range of IPs
        elif "-" in current:
            start, _, end = current.strip().partition('-')
            # If you are looking at this line wondering wtf give this a go: socket.inet_ntoa(struct.pack('>I', 5))
            return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(struct.unpack('>I', socket.inet_aton(start))[0], struct.unpack('>I', socket.inet_aton(end))[0])]
        # Single IP
        elif IpValidator.is_valid_ipv4_address(current):
            return [current]
        # Bad entry
        else:
            self.debug("Error: Invalid type, must be lower_ip-upper_ip or ip1, ip2, ip3, etc...")
            return None

    # Just an example - This takes ages on windows but is actually really fast under linux (<1s vs 8s)
    def get_port_state(self, target, port):
        # NMap
        nm = nmap.PortScanner()
        nm.scan(target, port)

        print('----------------------------------------------------')
        print('Host : %s (%s)' % (target, nm[target].hostname()))
        print('State : %s' % nm[target].state())
        for protocol in nm[target].all_protocols():
            print('----------')
            print('Protocol : %s' % protocol)
            specified_ports = nm[target][protocol].keys()
            specified_ports = sorted(specified_ports)
            for port in specified_ports:
                print('port : %s\tstate : %s' % (port, nm[target][protocol][port]['state']))

    def get_share(self, target, user, password, work_group):
        raw_shares = subprocess.run("net rpc share " +
                                    " -W " + work_group +
                                    " -I " + target +
                                    " -U " + user +
                                    "  % " + password,
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')
        self.debug(raw_shares)

    # NMAP scans for service and operating system detection
    def nmap(self, port_start, port_end):
        # TODO reduce dependency on self - unless usage can be justified.
        if self.quiet == "true":  # If quiet scan flag is set use "quiet" scan pre-sets

            if self.use_port_range == "true":  # If a port range has been specified use
                # "-p "start port"-"end port" in command
                command = "-p " + port_start + "-" + port_end + " -sV --version-light"
                self.nm.scan(hosts=self.ip_list, arguments=command)
            else:
                command = "-sV --version-light"
                self.nm.scan(hosts=self.ip_list, arguments=command)

            self.debug("NMAP command = " + " '" + self.nm.command_line() + "'")  # debug for printing the command
            self.nm.scan(hosts=self.ip_list, arguments="-O")
            self.debug("NMAP command = " + " '" + self.nm.command_line() + "'")

        else:  # Use "loud" scan pre-sets
            if self.use_port_range == "true":
                command = "-p " + port_start + "-" + port_end + " -sV --version-all -T4"
                self.nm.scan(hosts=self.ip_list, arguments=command)
            else:
                command = "-sV --version-all -T4"
                self.nm.scan(hosts=self.ip_list, arguments=command)

        self.debug("NMAP command = " + " '" + self.nm.command_line() + "'")
        self.nm.scan(hosts=self.ip_list, arguments="-O --osscan-guess -T5")
        self.debug("NMAP command = " + " '" + self.nm.command_line() + "'")

        return True

    def get_local_groups(self):
        # Part of net
        pass

    def get_domain_groups(self):
        # Also part of net
        pass

    def get_nbt_stat(self, target):
        raw_nbt = subprocess.run("nmblookup -A " + target, stdout=subprocess.PIPE).stdout.decode('utf-8')
        # Basically does the same as the real NBTSTAT but really really disgusting output



    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...

e = Enumerate(debug=True)
#e.nmap(str(1), str(100))
e.enumeration()
