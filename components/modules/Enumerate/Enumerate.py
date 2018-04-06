# This is why modules should share their package name.
import importlib
try:
    importlib.import_module("nmap")
except ImportError:
    import pip
    pip.main(['install', "python-nmap"])
finally:
    globals()["nmap"] = importlib.import_module("nmap")

import random
import struct
import subprocess
from collections import defaultdict

from components.framework.Debug import Debug
# from components.helpers.BlinktSupport import BlinktSupport
from components.helpers.Format import Format
from components.helpers.IpValidator import *
from components.helpers.ModuleManager import ModuleManager
from components.modules.Enumerate.Result2Html import result2html
from components.modules.Enumerate.TargetInfo import TargetInfo


# -.-. --- .-. . -.-- .... .- ... -. --- --. --- --- -.. .. -.. . .- ...


class Enumerate:
    def __init__(self, path, debug):
        self.enumerate = Debug(name="Enumerate", type="Module", debug=debug)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self.enumerate._name)
        if not self.current_config:
            self.enumerate.debug("Error: could not import config of " + self.enumerate._name, color=Format.color_danger)

        # Import default system path
        self.path = path

        # Import interface else use default
        self.interface = self.current_config.options["interface"] if self.current_config.options[
                                                                         "interface"] == "wlan0" or \
                                                                     self.current_config.options[
                                                                         "interface"] == "usb0" else "wlan0"
        self.enumerate.debug("Using interface: " + self.interface)

        # ~Produce list of usable ip addresses~
        ip_targets = self.current_config.options["ip_targets"]
        ip_exclusions = self.current_config.options["ip_exclusions"]
        self.ip_list = [ip for ip in self.get_ip_list(ip_targets) if ip not in self.get_ip_list(ip_exclusions)]

        # have to do it this way to avoid actions happening to both lists
        self.ip_list_shuffled = [ip for ip in self.ip_list]
        random.shuffle(self.ip_list_shuffled)

        # ~Produce list of usable ports~
        ports = self.current_config.options["port_targets"]
        port_exclusions = self.current_config.options["port_exclusions"]
        self.port_list = [port for port in self.get_port_list(ports) if port not in self.get_port_list(port_exclusions)]

        # ~Produce list of usable users.txt~
        self.user_list = []
        with open(self.path + "/modules/Enumerate/users.txt") as user_file:
            for line in user_file:
                user, _, password = line.strip().partition(":")
                self.user_list.append([user, password])

        # ~Produce list of default passwords~
        self.default_passwords = []
        with open(self.path + "/modules/Enumerate/default_passwords.txt") as password_file:
            for line in password_file:
                self.default_passwords.append(line)

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

    def run(self):
        # ~Runs all the things~
        # ---------------------
        target_ips = defaultdict()  # Init of dictionary


        current_ip_in_list = 1
        ips_in_list = len(self.ip_list_shuffled)

        for ip in self.ip_list_shuffled:  # Make it less obvious
            self.enumerate.debug("Target (%s) %s of %s" % (ip, current_ip_in_list, ips_in_list))

            current = TargetInfo()

            self.enumerate.debug("Starting ICMP", color=Format.color_info)
            # check current IP responds to ICMP
            current.RESPONDS_ICMP = self.check_target_is_alive(ip, interface=self.interface)
            self.enumerate.debug("%s responds to ICMP? %s" % (ip, current.RESPONDS_ICMP))

            self.enumerate.debug("Starting ARP", color=Format.color_info)
            # check current IP responds to ARP
            arp_response = self.get_targets_via_arp(ip, interface=self.interface)

            if arp_response is not False:
                try:
                    current.RESPONDS_ARP = True
                    current.MAC_ADDRESS = arp_response[0][1]
                    current.ADAPTER_NAME = arp_response[0][2]
                    self.enumerate.debug("%s responds to ARP? %s" % (ip, current.RESPONDS_ARP))
                    self.enumerate.debug("%s's physical address is %s" % (ip, current.MAC_ADDRESS))
                    self.enumerate.debug("%s's adapter name is %s" % (ip, current.ADAPTER_NAME))
                except Exception as Err:
                    self.enumerate.debug("Another error for corey: %s" % Err, color=Format.color_warning)
            else:
                self.enumerate.debug("No ARP response from %s" % ip)

            self.enumerate.debug("Starting Route", color=Format.color_info)
            # check route to this target
            if self.interface != "usb0":
                current.ROUTE = self.get_route_to_target(ip, map_host_names=False, interface=self.interface)
                self.enumerate.debug("Tracert to %s:\n %s" % (ip, current.ROUTE))

            # NBT STAT
            self.enumerate.debug("Starting NBTSTAT", color=Format.color_info)
            current.NBT_STAT = self.get_nbt_stat(ip)
            self.enumerate.debug("NBTSTAT for %s: %s" % (ip, current.NBT_STAT))

            # use all port scanning tools against current ip
            for port in self.port_list:
                pass
                # run things that use ports

            for user in self.user_list:
                pass
                # things that need users.txt

            # Use nmap to determine OS, port and service info then save to our current TargetInfo
            nmap_output = self.nmap()  # TODO portsCSV
            current.PORTS += (nmap_output[0])
            current.OS_INFO += (nmap_output[1])

            # self.other things that just uses IPs

            domaingroups, domainusers, domainpasswdpolicy = self.get_rpcclient(user_list=self.user_list, password_list=self.default_passwords, target=ip, ip=ip)
            #current.DOMAIN


            # Add target information to dict
            target_ips[ip] = current

            current_ip_in_list += 1

        # TODO use target_ips with Result2Html
        with open(self.path + "/modules/enumerate/output.html") as out:
            out.write(result2html(target_ips))

        return  # End of run

    def get_port_list(self, raw_ports):
        """
        :param raw_ports:
        :return list string?:
        :return none:
        """
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

        # Else Bad entry
        self.enumerate.debug(
            "Error: Invalid type, must be lower_port-upper_port, single port or p1, p2, p3, etc...")
        return None

    def get_ip_list(self, raw_ips):
        """
        :param raw_ips:
        :return list string:
        :return none:
        """
        # TODO 01/03/18 [2/2] Add error handling
        # Comma separated list of IPs
        if "," in raw_ips:
            return raw_ips.strip().split(',')
        # Range of IPs
        elif "-" in raw_ips:
            start, _, end = raw_ips.strip().partition('-')

            # If you are looking at this line wondering wtf give this a go: socket.inet_ntoa(struct.pack('>I', 5))
            return [socket.inet_ntoa(struct.pack('>I', i)) for i in
                    range(struct.unpack('>I', socket.inet_aton(start))[0],
                          struct.unpack('>I', socket.inet_aton(end))[0])]
        # Single IP
        elif IpValidator.is_valid_ipv4_address(raw_ips):
            return [raw_ips]
        # Bad entry
        else:
            self.enumerate.debug("Error: Invalid type, must be lower_ip-upper_ip or ip1, ip2, ip3, etc...")
            return None

    # This is not being called so I don't have usage example to work with
    def get_share(self, target, user, password, work_group):
        raw_shares = subprocess.run("net rpc share " +
                                    " -W " + work_group +
                                    " -I " + target +
                                    " -U " + user +
                                    "  % " + password,
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')
        self.enumerate.debug(raw_shares)

    # NMAP scans for service and operating system detection
    def nmap(self):
        """
        :return list of list of list of strings:
        :return none:
        """

        nm = nmap.PortScanner()  # Declare python NMAP object
        output_list = []  # List for saving the output of the commands to

        def service_parsing():  # local function for parsing service and port info

            parsed_output = []

            for protocol in nm[self.ip_list].all_protocols():

                for port in nm[self.ip_list][protocol]:
                    nmap_results = nm[self.ip_list][protocol][port]
                    parsed_output.append(
                        [str(port), nmap_results['product'], nmap_results['version'], nmap_results['state']])

            output_list.append(parsed_output)  # Add parsed data to the output list

            return

        def os_parsing(output):  # Local function for parsing OS information
            # (required as python NMAP OS isn't working correctly)

            parsed_output = []

            # Separating OS info and appending it to the output list
            for line in output.splitlines():
                if "OS" in line and "detection" not in line and "matches" not in line:

                    if "Aggressive OS guesses" in line:
                        new_line = line.strip('Aggressive OS guesses:').split(', ')
                        parsed_output.append(new_line)

                    elif "OS details" in line:
                        new_line = line.strip('OS details:')
                        parsed_output.append(new_line)

            output_list.append(parsed_output)

            return

        if self.quiet == "true":  # If quiet scan flag is set use "quiet" scan pre-sets
            command = "-sV --version-light"

            if self.use_port_range == "true":  # If a port range has been specified use
                nm.scan(hosts=self.ip_list, ports=self.port_list, arguments=command)
            else:
                nm.scan(hosts=self.ip_list, arguments=command)

                self.enumerate.debug(
                    "NMAP command = " + " '" + nm.command_line() + "'")  # debug for printing the command

            # Run "quiet" nmap OS scan and save output to a variable for parsing
            os_output = subprocess.run("nmap" + str(self.ip_list) + "-O", shell=True,
                                       stdout=subprocess.PIPE).stdout.decode('utf-8')

        else:  # Use "loud" scan pre-sets
            command = "-sV --version-all -T4"

            if self.use_port_range == "true":
                nm.scan(hosts=self.ip_list, ports=self.port_list, arguments=command)
            else:
                nm.scan(hosts=self.ip_list, arguments=command)

                self.enumerate.debug("NMAP command = " + " '" + nm.command_line() + "'")

            # Run "loud" nmap OS scan and save output to a variable for parsing
            os_output = subprocess.run("nmap" + str(self.ip_list) + "-O --osscan-guess -T5", shell=True,
                                       stdout=subprocess.PIPE).stdout.decode('utf-8')

        os_parsing(os_output)  # Call local function for nmap OS parsing
        service_parsing()  # Call local function for nmap service/port parsing
        return output_list  # return the output of scans in the form of a list

    def get_local_groups(self):
        # Part of net
        return

    def get_domain_groups(self):
        # Also part of net
        return

    def get_nbt_stat(self, target):
        """
        :return list string:
        """
        raw_nbt = subprocess.run(["sudo", "nmblookup", "-A", target], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        # Basically does the same as the real NBTSTAT but really really disgusting output
        if not raw_nbt:
            self.enumerate.debug("get_nbt_stat Error: nmblookup failed", color=Format.color_warning)
            return False

        # Fixing that output
        output = []
        for line in raw_nbt:
            # Get actual results

            try:
                result = re.search("\s+(\S+)\s+<(..)>\s+-\s+?(<GROUP>)?\s+?[A-Z]\s+?(<ACTIVE>)?", line)
                result = [res if res is not None else "" for res in result.groups()]  # Need to replace None type with ""
                if result:  # If any matches the regex

                    # Ignore the "Looking up status of [target]" line
                    if "up status of" in line:
                        continue

                    # No results found for target
                    if "No reply from" in line:
                        return False

                    for nbt_line in self.nbt_info:
                        service, hex_code, group, descriptor = nbt_line
                        # if we need to check service or not (this is empty for some fields)
                        if service:
                            if service in result[0] and hex_code in result[1] and group in result[2]:
                                output.append("%s %s" % (line, descriptor))
                                break
                        else:
                            if hex_code in result[1] and group == bool(result[2]):
                                output.append("%s %s" % (line, descriptor))
                                break
                else:  # If it didn't match the regex
                    self.enumerate.debug("get_nbt_stat: No match found", color=Format.color_info)
                    output.append("%s" % line)
            except Exception as what_went_wrong:
                self.enumerate.debug("Something went wrong %s" % what_went_wrong, color=Format.color_warning)

        self.enumerate.debug("get_nbt_stat: Output generated: %s" % output, color=Format.color_info)
        return output[2:]

    def get_rpcclient(self, user_list, password_list, target, ip):
        """
        :param user_list:
        :param password_list:
        :param target:
        :param ip:
        :return none:
        """
        # Pass usernames in otherwise test against defaults  # What defaults? -Corey
        for user in user_list.keys():
            raw_rpc = subprocess.Popen("rpcclient -U " + + " " + target + " -c 'lsaquery'", stdin=subprocess.PIPE,stdout=subprocess.PIPE).stdout.decode('utf-8')  # Shut it PEP8, 1 line over 2 lines is minging
            try:
                raw_rpc.stdin.write(user_list[user])
                if user_list[user] == "":
                    # password list is empty - use default
                    for password in password_list:
                        raw_rpc.stdin.write(password)

            except IOError as e:
                self.enumerate.debug("Error: get_rpcclient: %s" % e)

            raw_rpc.stdin.close()
            raw_rpc.wait()

            if "NT_STATUS_CONNECTION_REFUSED" in raw_rpc:
                # Unable to connect
                self.enumerate.debug("Error: get_rpcclient: Connection refused under - %s : %s" % user % user_list[user])
                return None
            elif "NT_STATUS_LOGON_FAILURE" in raw_rpc:
                # Incorrect username or password
                self.enumerate.debug(
                    "Error: get_rpcclient: Incorrect username or password under - %s : %s " % user % user_list[user])

                return None
            elif "rpcclient $>" in raw_rpc:
                raw_command = subprocess.run("enumdomgroups", stdout=subprocess.PIPE).stdout.decode('utf-8')
                users_or_groups = False
                # true = users.txt / false = groups
                domaininfo = self.extract_info_rpc(raw_command, ip, users_or_groups)

                raw_command = subprocess.run("enumdomusers", stdout=subprocess.PIPE).stdout.decode('utf-8')
                users_or_groups = True
                # true = users.txt / false = groups
                userinfo = self.extract_info_rpc(raw_command, ip, users_or_groups)

                raw_command = subprocess.run("getdompwinfo", stdout=subprocess.PIPE).stdout.decode('utf-8')
                passwdinfo = self.get_password_policy(raw_command, ip)

                return domaininfo, userinfo, passwdinfo
                # then run get_smbclient

            else:
                self.enumerate.debug("Error: get_rpcclient: No reply from target")
                return None

    def get_password_policy(self, raw_command, ip):
        """
        :param raw_command:
        :param ip:
        :return int, bool, bool, bool, bool, bool, bool:
        """
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

        return length, clear_text_pw, refuse_pw_change, lockout_admins, complex_pw, pw_no_change, pw_no_anon_change

    def extract_info_rpc(self, raw_command, ip, users_or_groups):
        """
        :param raw_command:
        :param ip:
        :param users_or_groups:
        :return list, list:
        """
        index = 0
        start = 0
        counter = 0
        users = []
        rids = []

        for char in raw_command:
            if char == "\n":
                counter += 1
        # Is this a diy regex? -Corey
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
        # users.txt = (ip, users.txt)
        # rids = (ip, rids)
        # current.DOMAIN.append(users.txt)
        # current.DOMAIN.append(rids)
        return users, rids


    def check_target_is_alive(self, target, interface="wlan0", ping_count=0, all_ips_from_dns=False, get_dns_name=False,
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

        command = ["fping", "-a", "-I ", interface]

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

        self.enumerate.debug("check_target_is_alive command is: %s" % command)

        if ping_count > 0:
            output = subprocess.run(command, stderr=subprocess.PIPE).stderr.decode("utf-8").strip().split("\n")
        else:
            output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").strip().split("\n")

        self.enumerate.debug("check_target_is_alive command output is: %s" % output)

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

        :return: 2 list of max 30 items with ips for each hop to the target and returning
                 List to target is a list of strings and List from target containing lists of strings
                 Bad hops / no information is signaled as '*'
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

        route_out = []
        route_back = []

        for line in output:
            line = line.split()
            del line[0]

            results = []  # init var to store current results
            if map_host_names:
                for item in line:
                    # If item looks like a domain or the first three octets of an IP address
                    if re.search("[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*",
                                 item.lower()):  # Would compiling a re be better here?
                        results += [item.strip("\(\)")]  # Remove any brackets and add to results for this line
            else:
                for item in line:
                    if IpValidator.is_valid_ipv4_address(item):
                        results += [item]

            if len(results) is 1:
                route_out += [results]  # Add results from this line
                route_back += []
            elif len(results) is not 0:
                route_out += [results[0]]
                route_back += [results[1:]]
            else:
                route_out += ["*"]
                route_back += [["*"]]

        if type(route_out[0]) is list:
            route_out[0] = route_out[0][0]

        return route_out, route_back

    def get_targets_via_arp(self, target, interface="usb0", source_ip="self", target_is_file=False,
                            original_out=False, randomise_targets=False):
        """
        Makes use of the arp-scan command.
        By default makes use of the verbose and retry flags.

        Target can be a list of IP's or a single IP.
            This allows for passing in the lists (such as that which the configs stores)
        :param target: IPv4 address(s) e.g "192.168.0.1", "192.168.0.0/24", ["192.168.0.1", "192.168.0.2"]

        :param interface: String value for interface, can make use of any interface that is available
                Defaults to "usb0"
        :param source_ip: String value that can be changed send packets with source being another address.
                Defaults to "self"
        :param target_is_file: Binary value for when the user wishes to use a file containing addresses.
                Defaults False
        :param original_out: Binary value for whether the command gives out the command output without parsing.
                Defaults False
        :param randomise_targets: Binary Value for targets where they should not be scanned in the order given.
                Defaults False

        :return: list of lists containing IP, MAC address and Adapter name


        """
        command = ["sudo", "arp-scan", "-v", "-I", interface, "-r", "3"]

        if randomise_targets:
            command += ['-R']

        if source_ip is not "self" and IpValidator.is_valid_ipv4_address(source_ip):
            command += ["-s", source_ip]

        if target_is_file is True:
            if target is list:
                self.enumerate.debug("Error: A list of files cannot be scanned", color=Format.color_warning)
                return False

            command += ["-f", target]  # The target in this case should be the path to a target list file

        else:  # if target is not a file
            if type(target) is list:
                for current in target:
                    if not IpValidator.is_valid_ipv4_address(current, iprange=True):
                        self.enumerate.debug("Error: Target %s in list is not a valid IP" % target, color=Format.color_warning)
                        return False

                command += target

            elif type(target) is str:  # if target is just an IP
                if not IpValidator.is_valid_ipv4_address(target, iprange=True):
                    self.enumerate.debug("Error: Target is not a valid IP or Range", color=Format.color_warning)
                    return False

                command += [target]

            else:
                self.enumerate.debug("Error: Target is not a string or list")
                return False

        self.enumerate.debug("get_targets_via_arp command is: %s" % command)

        output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

        self.enumerate.debug("get_targets_via_arp output captured: %s" % True if output else False)

        if original_out is True:
            return output

        output = output.splitlines()

        self.enumerate.debug("get_targets_via_arp generating results...")
        # Removing generalised information out
        try:
            del output[0:2]
            del output[-3:]


            outlist = []  # was unable to change each line from a string to a list so moving each line as it becomes a list

            for line in output:
                # Splits where literal tabs exist (between the IP, MAC and Adapter Name)
                outlist += [line.split("\t")]
        except Exception as Err:
            self.enumerate.debug("get_targets_via_arp Error: %s" % Err, color=Format.color_warning)
            return False
        return outlist  # Sorting via IP would be nice

    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...
