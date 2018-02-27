import subprocess

import nmap

from components.framework.Debug import Debug
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


class Enumerate(Debug):
    def __init__(self, debug=False):
        super().__init__(name="Enumerate", type="Module", debug=debug)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)
        if not self.current_config:
            self.debug("Error: could not import config of " + self._name)

        self.targets = self.current_config.options["targets"]

    # Just an example - This takes ages on windows but is actually really fast under linux (<1s vs 8s)
    def get_port_state(self, target, port_range="22-443"):
        # NMap
        nm = nmap.PortScanner()
        nm.scan(target, port_range)

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
        # TODO 1/2 test in lab as could not test at home

    def get_local_groups(self):
        # Part of net
        pass

    def get_domain_groups(self):
        # Also part of net
        pass

    def get_nbt_stat(self, target):
        raw_nbt = subprocess.run("nmblookup -A " + target, stdout=subprocess.PIPE).stdout.decode('utf-8')
        # Basically does the same as the real NBTSTAT but really really disgusting output
        # TODO 2/2 test in lab as could not test at home (Fully).


    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...


e = Enumerate(debug=True)
e.get_port_state("192.168.0.11", "80")