import yattag

from collections import defaultdict
from components.modules.Enumerate.TargetInfo import TargetInfo
from components.framework.Debug import Debug
from components.helpers.Format import Format


class Result2Html:

    def __init__(self, debug):
        self.result2html_dbg = Debug(name="Result2Html", type="Module/Enumerate/helper", debug=debug)
        self.result2html_dbg.debug("Initializing Result2Html")

    def result2html(self, targets, ip_list):
        """
        Description:
                    Converts Enumerate output to human-readable form

        :param targets:     List containing TargetInfo Objects
        :return:            Bootstrap-based HTML5 page of results
        """
        self.result2html_dbg.debug("Starting Result2Html...", color=Format.color_info)

        self.result2html_dbg.debug("TargetInfo output:")
        for dbg_ip in ip_list:
            info = targets[dbg_ip]
            self.result2html_dbg.debug("IP: %s" % dbg_ip)
            self.result2html_dbg.debug("Responds to ICMP: %s" % info.RESPONDS_ICMP)
            self.result2html_dbg.debug("Responds to ARP: %s" % info.RESPONDS_ARP)
            self.result2html_dbg.debug("MAC: %s" % info.MAC_ADDRESS)
            self.result2html_dbg.debug("Adapter name: %s" % info.ADAPTER_NAME)
            self.result2html_dbg.debug("Route to %s: %s" % (dbg_ip, info.ROUTE))
            self.result2html_dbg.debug("OS info: %s" % info.OS_INFO)
            self.result2html_dbg.debug("Software info: %s" % info.SOFTWARE_INFO)
            self.result2html_dbg.debug("Workgroup info: %s" % info.WORKGROUP)
            self.result2html_dbg.debug("Domain info: %s" % info.DOMAIN)
            self.result2html_dbg.debug("Local info: %s" % info.LOCAL)
            self.result2html_dbg.debug("Session info: %s" % info.SESSIONS)
            self.result2html_dbg.debug("NBT info: %s" % info.NBT_STAT)
            self.result2html_dbg.debug("Share info %s" % info.SHARE_INFO)
            self.result2html_dbg.debug("Password policy: %s" % info.PASSWD_POLICY)
            self.result2html_dbg.debug("Printer info: %s" % info.PRINTER_INFO)
            self.result2html_dbg.debug("Port info: %s" % info.PORTS)

        self.result2html_dbg.debug("Beginning html parsing", color=Format.color_info)

        doc, tag, text = yattag.Doc().tagtext()
        doc.asis('<!DOCTYPE html>')

        with tag('html', lang="en"):
            with tag('head'):
                doc.asis('<meta charset="utf-8">')
                doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
                doc.asis('<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">')
                with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
                    pass
                with tag('script', src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"):
                    pass
                with tag('body'):
                    with tag('div', klass="container"):
                        # Table for current IP
                        for IP in ip_list:  # Read Ips from list so that they are in order
                            # Basic Info
                            with tag("h3"):
                                text("%s Basic Info" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text(IP)
                                        with tag('th'):
                                            text("Info")
                                # Table rows
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Responds to ICMP")
                                        with tag('td'):
                                            text("True" if targets[IP].RESPONDS_ICMP else "False")
                                    with tag('tr'):
                                        with tag('td'):
                                            text("MAC Address")
                                        with tag('td'):
                                            text(targets[IP].MAC_ADDRESS if targets[IP].MAC_ADDRESS else "None")
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Adapter name")
                                        with tag('td'):
                                            text(targets[IP].ADAPTER_NAME if targets[IP].ADAPTER_NAME else "None")

                            # Route
                            with tag("h3"):
                                text("Route to %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("HOP #")
                                        with tag('th'):
                                            text(IP)
                                # Table rows
                                for index, value in targets[IP].ROUTE:
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td'):
                                                text(index)  # hop
                                            with tag('td'):
                                                text(value)  # ip
                            # OS Info
                            with tag("h3"):
                                text("OS Info for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Suspected OS ")

                                with tag('tbody'):
                                    # Table rows
                                    # TODO check that not list of suspected OS rather than list of list of suspected OS
                                    for lists in targets[IP].OS_INFO:
                                        for suspected_os in lists:
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(suspected_os)

                            # SOFTWARE INFO
                            with tag("h3"):
                                text("Software Info for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Software Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # WORKGROUP
                            with tag("h3"):
                                text("Workgroup Info for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Workgroup Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # DOMAIN
                            with tag("h3"):
                                text("Domain Info for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Domain Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # LOCAL
                            with tag("h3"):
                                text("Local Info for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Local Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # SESSIONS
                            with tag("h3"):
                                text("%s Sessions" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Session Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # NBT STAT
                            with tag("h3"):
                                text("%s NBT Stat" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("NBT STAT Info")
                                with tag('tbody'):
                                    for NBT_INFO in targets[IP].NBT_STAT:
                                        with tag('tr'):
                                            with tag('td'):
                                                text(NBT_INFO)

                            # SHARE INFO
                            with tag("h3"):
                                text("%s Share Info" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Share Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # SHARE INFO
                            with tag("h3"):
                                text("%s Share Info" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Local Info")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # PASSWD POLICY
                            with tag("h3"):
                                text("%s Password Policy" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Password Policy")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # Printer Info
                            with tag("h3"):
                                text("%s Printer Info" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Password Policy")
                                with tag('tbody'):
                                    with tag('tr'):
                                        with tag('td'):
                                            text("Not currently implemented :(")

                            # PORTS
                            with tag("h3"):
                                text("Ports for %s" % IP)
                            with tag('table', klass="table table-condensed"):
                                # Table headings
                                # Port Service Version State
                                with tag('thead'):
                                    with tag('tr'):
                                        with tag('th'):
                                            text("Port")
                                        with tag('th'):
                                            text("Service")
                                        with tag('th'):
                                            text("Version")
                                        with tag('th'):
                                            text("State")
                                with tag('tbody'):
                                    with tag('tr'):
                                        for lists in targets[IP].PORTS:
                                            for port, service, version, state in lists:
                                                with tag('td'):
                                                    text(port)
                                                with tag('td'):
                                                    text(service)
                                                with tag('td'):
                                                    text(version)
                                                with tag('td'):
                                                    text(state)

        return yattag.indent(doc.getvalue())
