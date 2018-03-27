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
        self.RESPONDS_ICMP = False
        self.RESPONDS_ARP = False
        self.MAC_ADDRESS = ""
        self.ADAPTER_NAME = ""
        self.ROUTE = []
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
    def __init__(self, path, debug=False):
        super().__init__(name="Enumerate", type="Module", debug=debug)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)
        if not self.current_config:
            self.debug("Error: could not import config of " + self._name)

        # Import default system path
        self.path = path

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
        self.interface = "wlan0"  # Didn't ammend to the ini as Im not sure if its as simple as adding interface = "foo"
                                  # under the option section but its something TODO

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
        targets = ()  # Init of Dictionary?

        for ip in self.ip_list:
            current = TargetInfo()

            # check current IP responds to ICMP
            self.check_target_is_alive(current, interface=self.interface)

            # check current IP responds to ARP
            arp_response = self.get_targets_via_arp(current, interface=self.interface)

            if arp_response is not None:
                current.RESPONDS_ARP = True
                current.MAC_ADDRESS = arp_response[1]
                current.ADAPTER_NAME = arp_response[2]

            # check route to this target
            current.ROUTE = self.get_route_to_target(ip, map_host_names=False, interface=self.interface)

            # use all port scanning tools against current ip
            for port in self.port_list:
                # run things that use ports
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
        elif 0 <= int(raw_ports) <= 65535:
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

        current = TargetInfo
        users = (ip, users)
        rids = (ip, rids)
        current.DOMAIN.append(users)
        current.DOMAIN.append(rids)

    @staticmethod
    def check_target_is_alive(target, interface="usb0", ping_count=0, all_ips_from_dns=False, get_dns_name=False,
                              contain_random_data=True, randomise_targets=False, source_address="self", verbose=False):
        """
        Uses ICMP pings to check that hosts are online/responsive. This makes use of the FPing command line tool so is
        able to ping multiple hosts

        :param target: Either target via IPv4, IPv4 range, list of IPv4's, DNS Name(s?!)
        :param interface: Choose which interface the pings go from. Defaults to USB0
        :param ping_count: Will ping as many times as the input asks for
        :param all_ips_from_dns: Scans all IP address's relating to that DNS name
        :param get_dns_name: Will return with the DNS name for the IP scanned
        :param contain_random_data: Will not just send empty packets like the default
        :param randomise_targets: Will go through the targets provided in a random order
        :param source_address: Changes where the ping says it came from
        :param verbose: Only really effects the ping count command. Swaps output from RTTimes to Statistics

        :return: list of IP's that were seen to be alive
        """

        command = ["fping", "-a", "--iface=" + interface]

        # Adding Flags
        if ping_count > 0:
            if verbose:
                command += ["-D", "--count=" + str(ping_count)]
            else:
                command += ["--vcount=" + str(ping_count)]

        if get_dns_name:
            command += ["-n"]

        if randomise_targets:
            command += ["--random"]

        if contain_random_data:
            command += ["-R"]

        if source_address is not "self":
            if IpValidator.is_valid_ipv4_address(source_address):
                command += ["--src=" + source_address]
            else:
                return "Error: The redirection should be to a IPv4"

        # Adding Targets
        if type(target) is list:
            if all_ips_from_dns:
                for item in target:
                    if not re.search("\A[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*", item.lower()):
                        return "Error: Target in list is not a valid IP or hostname (Does not accept ranges here)"
            else:
                for item in target:
                    if not IpValidator.is_valid_ipv4_address(item):
                        return "Error: Target in list is not a valid IP (Does not accept ranges here)"

            command += target

        elif IpValidator.is_valid_ipv4_address(str(target)):
            command += [target]

        elif IpValidator.is_valid_ipv4_address(str(target), iprange=True):
            command += ["-g", target]

        elif re.search("\A[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*\Z", str(target).lower()) and all_ips_from_dns:
            command += ["-m", target]
        else:
            return "Error: Target is not a valid IP, Range or list"

        if ping_count > 0:
            output = subprocess.run(command, stderr=subprocess.PIPE).stderr.decode("utf-8").strip().split("\n")
        else:
            output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").strip().split("\n")

        if not output:
            return None

        if source_address is not "self":
            return None

        if ping_count > 0:
            final_out = [[]]

            if verbose:
                # This is not working. It cuts the min/avg/max section of the out and I cant be arsed fixing it
                for line in output:
                    final_out += [line.split(" : ")]
            else:
                for line in output:
                    temp = line.split(" : ")
                    temp[1] = temp[1].split()
                    final_out += [temp]

            del final_out[0]
            return final_out

        return output

    @staticmethod
    def get_route_to_target(target, interface="usb0", bypass_routing_tables=False, hop_back_checks=True,
                            map_host_names=True, original_out=False):
        """
        Makes use of the traceroute command.
        No default flags are in use that the user cannot access via output

        Args:
        :param target: takes in a IPv4 target (Cannot Take a list)
        :param interface: Defaults to usb0 but can make use of any interface that is available
        :param bypass_routing_tables: Allows for traceroute to take the most direct approach bypassing routing tables
        :param hop_back_checks: Confirms that packets taken by the response follow the same path
        :param map_host_names: In the event that mapping host names to IP makes noise this can be disabled
        :param original_out: If the user wants the original command output this should be changed to true

        :return: list of ip lists for each hop. Often single item list but keeps consistent for accessing
        """
        command = ["traceroute", "-i", interface]  # start with command items that are required

        # Add command arguments where appropriate
        if bypass_routing_tables:
            command += ["-r"]

        if hop_back_checks:
            command += ["--back"]

        if not map_host_names:
            command += ["-n"]

        if type(target) is str:
            if IpValidator.is_valid_ipv4_address(target):
                command += [target]
        else:
            return "Error: Wrong type"  # Trace route is not able to target multiple hosts

        # Running command
        output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

        if original_out is True:  # If user doesnt want output parsed
            return output

        # Parsing output
        output = output.splitlines()

        del output[0]

        output_out = []

        if map_host_names:
            for line in output:
                results = []  # init var to store current results
                line = line.split()
                del line[0]

                for item in line:
                    # If item looks like a domain or the first three octets of an IP address
                    if re.search("[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*",
                                 item.lower()):  # Would compiling a re be better here?
                        results += [item.strip("\(\)")]  # Remove any brackets and add to results for this line

                if IpValidator.is_valid_ipv4_address(results[0]):  # If the "Host name" is an IP
                    results = results[::2]  # Grab every other variable

                output_out += [results]  # Add results from this line

        else:
            for line in output:
                results = []  # init var to store current results
                line = line.split()
                del line[0]

                for item in line:
                    if IpValidator.is_valid_ipv4_address(item):
                        results += [item]
                output_out += [results]

        return output_out

    @staticmethod
    def get_targets_via_arp(target, interface="usb0", source_ip="self", target_is_file=False,
                            original_out=False, randomise_targets=False):
        """
        Makes use of the arp-scan command.
        By default makes use of the verbose and retry flags.

        Target can be a list of IP's or a single IP.
            This allows for passing in the lists (such as that which the configs stores)
        :param target: IPv4 address(s) e.g "192.168.0.1", "192.168.0.0/24", ["192.168.0.1", "192.168.0.2"]
        :param interface: String value for interface, defaults to usb0 but can make use of any interface that is available
        :param source_ip: String value that defaults to self but can be changed send packets with source being another address
        :param target_is_file: Binary value for when the user wishes to use a file containing addresses. Defaults False
        :param original_out: Binary value for whether the command gives out the command output without parsing. Defaults False
        :param randomise_targets: Binary Value for targets where they should not be scanned in the order given. Defaults False

        :return: output of the command to be parsed
        """
        command = ["arp-scan", "-v", "-I", interface, "-r", "3"]

        if randomise_targets:
            command += ['-R']

        if source_ip is not "self" and IpValidator.is_valid_ipv4_address(source_ip):
            command += ["-s", source_ip]

        if target_is_file is True:
            if target is list:
                return "Error: A list of files cannot be scanned"

            command += ["-f", target]  # The target in this case should be the path to a target list file

        else:  # if target is not a file
            if type(target) is list:
                for current in target:
                    if not IpValidator.is_valid_ipv4_address(current, iprange=True):
                        return "Error: Target " + str(current) + " in list is not a valid IP"

                command += target

            elif type(target) is str:  # if target is just an IP
                if not IpValidator.is_valid_ipv4_address(target, iprange=True):
                    return "Error: Target is not a valid IP or Range"

                command += [target]

            else:
                return "Error: Target is not a string or list"

        output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

        if original_out is True:
            return output

        output = output.splitlines()

        # Removing generalised information out
        del output[0:2]
        del output[-3:]

        outlist = [
            []]  # was unable to change each line from a string to a list so moving each line as it becomes a list

        for line in output:
            # Splits where literal tabs exist (between the IP, MAC and Adapter Name)
            outlist += [line.split("\t")]

        return outlist  # Sorting via IP would be nice

    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...
