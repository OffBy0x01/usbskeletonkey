import re
import struct
import subprocess

from components.framework.Debug import Debug
from components.helpers.IpValidator import *
from components.helpers.ModuleManager import ModuleManager
from components.helpers.nmap import nmap  # TODO Find a fix on Pi that doesn't require local storage of import


class TargetInfo:
    """
    To be used with Run to create a tuple of (TargetIP, TargetInfo) for each target ip
    """
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
        self.PORTS = []  # prolly formatted like this "PORT_NUMBER, SERVICE, STATUS"
# -.-. --- .-. . -.-- .... .- ... -. --- --. --- --- -.. .. -.. . .- ...


class Enumerate(Debug):
    def __init__(self, debug=False):
        super().__init__(name="Enumerate", type="Module", debug=debug)


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

        # # ~Produce list of usable users~
        # self.user_list = []
        # with open("user_list.txt") as user_file:
        #     for line in user_file:
        #         user, _, password = line.strip().partition(":")
        #         self.user_list.append({user: password})

        self.quiet = self.current_config.options["quiet"]
        self.verbose = self.current_config.options["verbose"]
        self.use_port_range = self.current_config.options["use_port_range"]

        ###############################################################################
        # The following  mappings for nmblookup (nbtstat) status codes to human readable
        # format is taken from nbtscan 1.5.1 "statusq.c".  This file in turn
        # was derived from the Samba package which contains the following
        # license:
        #    Unix SMB/Netbios implementation
        #    Version 1.9
        #    Main SMB server routine
        #    Copyright (C) Andrew Tridgell 1992-1999
        #
        #    This program is free software; you can redistribute it and/or modif
        #    it under the terms of the GNU General Public License as published b
        #    the Free Software Foundation; either version 2 of the License, o
        #    (at your option) any later version
        #
        #    This program is distributed in the hope that it will be useful
        #    but WITHOUT ANY WARRANTY; without even the implied warranty o
        #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See th
        #    GNU General Public License for more details
        #
        #    You should have received a copy of the GNU General Public Licens
        #    along with this program; if not, write to the Free Softwar
        #    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA

        self.nbt_info = [
            ["__MSBROWSE__", "01", 0, "Master Browser"],
            ["INet~Services", "1C", 0, "IIS"],
            ["IS~", "00", 1, "IIS"],
            ["", "00", 1, "Workstation Service"],
            ["", "01", 1, "Messenger Service"],
            ["", "03", 1, "Messenger Service"],
            ["", "06", 1, "RAS Server Service"],
            ["", "1F", 1, "NetDDE Service"],
            ["", "20", 1, "File Server Service"],
            ["", "21", 1, "RAS Client Service"],
            ["", "22", 1, "Microsoft Exchange Interchange(MSMail Connector)"],
            ["", "23", 1, "Microsoft Exchange Store"],
            ["", "24", 1, "Microsoft Exchange Directory"],
            ["", "30", 1, "Modem Sharing Server Service"],
            ["", "31", 1, "Modem Sharing Client Service"],
            ["", "43", 1, "SMS Clients Remote Control"],
            ["", "44", 1, "SMS Administrators Remote Control Tool"],
            ["", "45", 1, "SMS Clients Remote Chat"],
            ["", "46", 1, "SMS Clients Remote Transfer"],
            ["", "4C", 1, "DEC Pathworks TCPIP service on Windows NT"],
            ["", "52", 1, "DEC Pathworks TCPIP service on Windows NT"],
            ["", "87", 1, "Microsoft Exchange MTA"],
            ["", "6A", 1, "Microsoft Exchange IMC"],
            ["", "BE", 1, "Network Monitor Agent"],
            ["", "BF", 1, "Network Monitor Application"],
            ["", "03", 1, "Messenger Service"],
            ["", "00", 0, "Domain/Workgroup Name"],
            ["", "1B", 1, "Domain Master Browser"],
            ["", "1C", 0, "Domain Controllers"],
            ["", "1D", 1, "Master Browser"],
            ["", "1E", 0, "Browser Service Elections"],
            ["", "2B", 1, "Lotus Notes Server Service"],
            ["IRISMULTICAST", "2F", 0, "Lotus Notes"],
            ["IRISNAMESERVER", "33", 0, "Lotus Notes"],
            ['Forte_$ND800ZA', "20", 1, "DCA IrmaLan Gateway Server Service"]
        ]
        # ~end of enum4linux.pl-derived code~

    # ~Runs all the things~
    # ---------------------
    def run(self):
        targets = ()
        for ip in self.ip_list:
            current = TargetInfo()
            for port in self.port_list:
                # things that use ports
                current.PORTS.append(self.get_port_state())
                pass

            for user in self.user_list:
                # things that need users
                pass

            #  self.other things that just uses IPs

            # Use nmap to determine OS, port and service info then save to a list
            nmap_output = self.nmap()  # TODO portsCSV
            current.OS_INFO.append(nmap_output[0])
            current.PORTS.append(nmap_output[1])

            # Add target information TODO Evaluate less memory intensive methods
            targets += (ip, current)

    def get_port_list(self, raw_ports):
        # TODO 01/03/18 [1/2] Add error handling
        # Comma separated list of Ports
        if "," in raw_ports:
            return raw_ports.strip().split(',')
        # Range of ports
        elif "-" in raw_ports:
            start, _, end = raw_ports.strip().partition('-')
            return [port for port in range(int(start), int(end))]
        # Single port
        elif raw_ports >= 0 and raw_ports <= 65535:
            return [raw_ports]
        # Bad entry
        else:
            self.debug("Error: Invalid type, must be lower_port-upper_port, single port or p1, p2, p3, etc...")
            return None

    def get_ip_list(self, raw_ips):
        # TODO 01/03/18 [2/2] Add error handling
        # Comma separated list of IPs
        if "," in raw_ips:
            return raw_ips.strip().split(',')
        # Range of IPs
        elif "-" in raw_ips:
            start, _, end = raw_ips.strip().partition('-')

            # If you are looking at this line wondering wtf give this a go: socket.inet_ntoa(struct.pack('>I', 5))
            return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(struct.unpack('>I', socket.inet_aton(start))[0], struct.unpack('>I', socket.inet_aton(end))[0])]
        # Single IP
        elif IpValidator.is_valid_ipv4_address(raw_ips):
            return [raw_ips]
        # Bad entry
        else:
            self.debug("Error: Invalid type, must be lower_ip-upper_ip or ip1, ip2, ip3, etc...")
            return None

    # Just an example - This takes ages on windows but is actually really fast under linux (<1s vs 8s)
    def get_port_state(self, target, port):
        # NMap
        nm = nmap.PortScanner()
        nm.scan(target, port)
        protocol = nm[target].all_protocols()[0]
        return [port, protocol, nm[target][protocol][port]['state']]

    def get_share(self, target, user, password, work_group):
        raw_shares = subprocess.run("net rpc share " +
                                    " -W " + work_group +
                                    " -I " + target +
                                    " -U " + user +
                                    "  % " + password,
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')
        self.debug(raw_shares)

    # NMAP scans for service and operating system detection
    def nmap(self):

        nm = nmap.PortScanner()  # Declare python NMAP object
        output_list = []  # List for saving the output of the commands to

        def service_parsing():  # local function for parsing service and port info

            parsed_output = ''

            for protocol in nm[self.ip_list].all_protocols():

                for port in nm[self.ip_list][protocol]:
                    nmap_results = nm[self.ip_list][protocol][port]

                    #  Add output to variable
                    parsed_output += (('PORT: ' + str(port) + ': ' + "SERVICE: " + nmap_results['product']
                                + " VERSION: " + nmap_results['version'] + " STATE: " + nmap_results['state']) + '\n')

            output_list.append(parsed_output)  # Add parsed data to the output list

            return

        def os_parsing(output):  # Local function for parsing OS information
            # (required as python NMAP OS isn't working correctly)

            parsed_output = ''

            # Separating OS info and appending it to the output list
            for line in output.splitlines():

                if "OS" in line and "detection" not in line and "matches" not in line:

                    if "Aggressive OS guesses" in line:
                        new_line = line.replace(',', '\n')
                        new_line = new_line.replace('Aggressive OS guesses:', '')
                        parsed_output = (parsed_output + '\n' + new_line)  # Save output to a variable

                    elif "OS CPE" in line or "OS details":
                        new_line = line.strip('OS CPE:')
                        new_line = new_line.strip('OS details: ')
                        parsed_output = (parsed_output + '\n' + new_line)  # Save output to a variable

            super().debug(parsed_output)  # Debug

            output_list.append(parsed_output)

            return

        if self.quiet == "true":  # If quiet scan flag is set use "quiet" scan pre-sets
            command = "-sV --version-light"

            if self.use_port_range == "true":  # If a port range has been specified use
                nm.scan(hosts=self.ip_list, ports=self.port_list, arguments=command)
            else:
                nm.scan(hosts=self.ip_list, arguments=command)

            self.debug("NMAP command = " + " '" + nm.command_line() + "'")  # debug for printing the command

            # Run "quiet" nmap OS scan and save output to a variable for parsing
            os_output = subprocess.run("nmap" + str(self.ip_list) + "-O", shell=True,
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')

        else:  # Use "loud" scan pre-sets
            command = "-sV --version-all -T4"

            if self.use_port_range == "true":
                nm.scan(hosts=self.ip_list, ports=self.port_list, arguments=command)
            else:
                nm.scan(hosts=self.ip_list, arguments=command)

            self.debug("NMAP command = " + " '" + nm.command_line() + "'")

            # Run "loud" nmap OS scan and save output to a variable for parsing
            os_output = subprocess.run("nmap" + str(self.ip_list) + "-O --osscan-guess -T5", shell=True,
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')

        os_parsing(os_output)  # Call local function for nmap OS parsing
        service_parsing()  # Call local function for nmap service/port parsing
        return output_list  # return the output of scans in the form of a list

    def get_local_groups(self):
        # Part of net
        pass

    def get_domain_groups(self):
        # Also part of net
        pass

    def get_nbt_stat(self, target="127.0.0.1"):
        raw_nbt = subprocess.run("nmblookup -A " + target, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        # Basically does the same as the real NBTSTAT but really really disgusting output

        # Fixing that output
        output = []
        for line in raw_nbt:
            # Get actual results
            result = re.search("\s+(\S+)\s+<(..)>\s+-\s+?(<GROUP>)?\s+?[A-Z]\s+?(<ACTIVE>)?", line)
            if result:  # If it matches the regex
                result = [res if not None else "" for res in result.groups()]  # Need to replace None type with ""
                print(result)

                # Ignore the "Looking up status of [target]" line
                if "up status of" in line:
                    print("nbtstat for ", target, ":", sep="")
                    continue
                # No results found for target
                elif target in line:
                    break
                for nbt_line in self.nbt_info:
                    service, hex_code, group, descriptor = nbt_line
                    # if we need to check service or not (this is empty for some fields)
                    if service:
                        if service in result[0] and hex_code in result[1] and group in result[2]:
                            output.append("%s %s" % (line, descriptor))
                            break
                    else:
                        if hex_code in result[1] and group in result[2]:
                            output.append("%s %s" % (line, descriptor))
                            break
            else:  # If it didn't match the regex
                output.append("%s" % line)

        return output

    def get_rpcclient(self, user_list, password_list, target, ip):
        # Pass usernames in otherwise test against defaults
        for user in user_list:
            for password in password_list:
                subprocess.run("rpcclient -U " + user + " " + target + " -c 'lsaquery' 2>&1",
                               stdout=subprocess.PIPE).stdout.decode('utf-8')
                # enter password
                raw_rpc = subprocess.run(password).stdout.decode('utf-8')

                if "NT_STATUS_CONNECTION_REFUSED" in raw_rpc:
                    # Unable to connect
                    print("Connection refused under - " + user + ":" + password)
                elif "NT_STATUS_LOGON_FAILURE" in raw_rpc:
                    # Incorrect username or password
                    print("Incorrect username or password under -  " + user + ":" + password)
                elif "rpcclient $>" in raw_rpc:
                    raw_command = subprocess.run("enumdomgroups", stdout =subprocess.PIPE).stdout.decode('utf-8')
                    users_or_groups = False
                    # true = users / false = groups
                    self.extract_info_rpc(raw_command, ip, users_or_groups)

                    raw_command = subprocess.run("enumdomusers", stdout =subprocess.PIPE).stdout.decode('utf-8')
                    users_or_groups = True
                    # true = users / false = groups
                    self.extract_info_rpc(raw_command, ip, users_or_groups)

                    raw_command = subprocess.run("getdompwinfo", stdout=subprocess.PIPE).stdout.decode('utf-8')
                    self.get_password_policy(raw_command, ip)

                    # then run get_smbclient


                else:
                    print("No reply")

    def get_password_policy(self, raw_command, ip):
        length = 0
        clear_text_pw = False
        refuse_pw_change = False
        lockout_admins = False
        complex_pw = False
        pw_no_anon_change = False
        pw_no_change = False

        if "min_password_length" in raw_command:
            for s in raw_command.split():
                if s.isdigit():
                    length = s
        if "DOMAIN_PASSWORD_STORE_CLEARTEXT" in raw_command:
            clear_text_pw = True
        if "DOMAIN_REFUSE_PASSWORD_CHANGE" in raw_command:
            refuse_pw_change = True
        if "DOMAIN_PASSWORD_LOCKOUT_ADMINS" in raw_command:
            lockout_admins = True
        if "DOMAIN_PASSWORD_COMPLEX" in raw_command:
            complex_pw = True
        if "DOMAIN_PASSWORD_NO_ANON_CHANGE" in raw_command:
            pw_no_anon_change = True
        if "DOMAIN_PASSWORD_NO_CLEAR_CHANGE" in raw_command:
            pw_no_change = True

        current = TargetInfo()
        password_policy = (
        ip, length, clear_text_pw, refuse_pw_change, lockout_admins, complex_pw, pw_no_change, pw_no_anon_change)
        current.PASSWD_POLICY.append(password_policy)

    def extract_info_rpc(self, raw_command, ip, users_or_groups):
        index = 0
        start = 0
        counter = 0
        users = []
        rids = []

        for char in raw_command:
            if char == "\n":
                counter += 1
        for times in range(0, counter + 1):
            start = index
            start = raw_command.find('[', index)
            start += 1
            end = raw_command.find(']', start)
            users.append(raw_command[start:end])
            index = end

            start = raw_command.find('[', index)
            start += 1
            end = raw_command.find(']', start)
            rids.append(raw_command[start:end])
            index = end
            times += 1

        current = TargetInfo()
        if users_or_groups:
            users = (ip, users)
            user_rids = (ip, rids)
            current.DOMAIN.append(users)
            current.DOMAIN.append(user_rids)
        else:
            groups = (ip, users)
            user_rids = (ip, rids)
            current.DOMAIN.append(groups)
            current.DOMAIN.append(user_rids)

    def get_smbclient(self, users, target):
        # Pass usernames in otherwise test against defaults
        raw_smb = subprocess.run("smbclient // "+target+" / ipc$ -U"+users+" - c 'help' 2>&1", stdout=subprocess.PIPE).stdout.decode('utf-8')


    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...

e = Enumerate(debug=True)
#e.nmap(str(1), str(100))
#e.enumeration()
e.get_nbt_stat()