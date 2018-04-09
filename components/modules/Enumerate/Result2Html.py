import yattag
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

        password_policy_items = [["Password Min Length is", "MIN_PASSWORD_LENGTH"],
                                 ["Passwords Stored in Plaintext", "DOMAIN_PASSWORD_STORE_CLEARTEXT"],
                                 ["No need for weekly password changes", "DOMAIN_REFUSE_PASSWORD_CHANGE"],
                                 ["Has Admin been locked out from remote logons", "DOMAIN_PASSWORD_LOCKOUT_ADMINS"],
                                 ["Password Must be Complex", "DOMAIN_PASSWORD_COMPLEX"],
                                 ["Password Cannot be changed without logging on", "DOMAIN_PASSWORD_NO_ANON_CHANGE"],
                                 ["No logons that exchange passwords via plaintext", "DOMAIN_PASSWORD_NO_CLEAR_CHANGE"]]

        self.result2html_dbg.debug("Starting Result2Html...", color=Format.color_info)

        doc, tag, text = yattag.Doc().tagtext()

        self.result2html_dbg.debug("Beginning html formatting", color=Format.color_info)

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
                                self.result2html_dbg.debug("ICMP, MAC & Adapter")
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
                            self.result2html_dbg.debug(
                                "Formatting route to target %s" % self.result2html_dbg.recursive_type(targets[IP].ROUTE))
                            if targets[IP].ROUTE:
                                with tag("h3"):
                                    text("Route to %s" % IP)
                                with tag("h5"):
                                    text("'*' is used to signify a failed jump")
                                with tag("h5"):
                                    text("Return path populate where applicable")
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("HOP #")
                                            with tag('th'):
                                                text("IP/Domain Path Out")
                                            with tag('th'):
                                                text("IP/Domain Other Return Path(s)")
                                        # Table rows
                                        with tag('tbody'):
                                            for index, value in enumerate(targets[IP].ROUTE[0]):
                                                with tag('tr'):
                                                    with tag('td'):
                                                        text(1 + index)  # hop
                                                    with tag('td'):
                                                        text(value)  # ip
                                                    with tag('td'):
                                                        if targets[IP].ROUTE[1]:
                                                            routeout = ""
                                                            for ip in targets[IP].ROUTE[1][index]:
                                                                routeout += "%s, " % ip
                                                            text(routeout[:-2])
                                                        else:
                                                            text("*")

                            # OS Info
                            self.result2html_dbg.debug("Formatting OS INFO")
                            if targets[IP].OS_INFO:
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Suspected OS ")

                                    with tag('tbody'):
                                        # Table rows
                                        # TODO check that not list of suspected OS rather than list of list of suspected OS
                                        if targets[IP].OS_INFO:
                                            for suspected_os in targets[IP].OS_INFO:
                                                with tag('tr'):
                                                    with tag('td'):
                                                        text(suspected_os)
                                        else:
                                            with tag('tr'):
                                                with tag('td'):
                                                    text("No results")

                            # SOFTWARE INFO
                            self.result2html_dbg.debug("Formatting Software INFO")
                            if targets[IP].SOFTWARE_INFO:
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
                            self.result2html_dbg.debug("Workgroup not implemented")
                            if targets[IP].WORKGROUP:
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

                            # Domain Groups
                            self.result2html_dbg.debug("Formatting Domain groups ")
                            if targets[IP].DOMAIN_GROUPS:
                                with tag("h4"):
                                    text("Domain Groups for %s" % IP)
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Groups")
                                            with tag('th'):
                                                text("RID")
                                    with tag('tbody'):
                                        for item in targets[IP].DOMAIN_GROUPS:
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(item[0])
                                                with tag('td'):
                                                    text(item[1])

                            # Domain Users
                            self.result2html_dbg.debug("Formatting Domain users")
                            if targets[IP].DOMAIN_USERS:
                                with tag("h4"):
                                    text("Domain Users for %s" % IP)
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Username")
                                            with tag('th'):
                                                text("RID")
                                    with tag('tbody'):
                                        for item in targets[IP].DOMAIN_USERS:
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(item[0])
                                                with tag('td'):
                                                    text(item[1])

                            # SESSIONS
                            self.result2html_dbg.debug("Formatting Sessions")
                            if targets[IP].SESSIONS:
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
                            self.result2html_dbg.debug("Formatting NBT STAT")
                            if targets[IP].NBT_STAT:
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
                            self.result2html_dbg.debug("Formatting Shares")
                            if targets[IP].SHARE_INFO:
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Sharename")
                                            with tag('th'):
                                                text("Type")
                                            with tag('th'):
                                                text("Comment")
                                    with tag('tbody'):
                                        for x in range(len(targets[IP].SHARE_INFO)):
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(targets[IP].SHARE_INFO[0][x])
                                                with tag('td'):
                                                    text(targets[IP].SHARE_INFO[1][x])
                                                with tag('td'):
                                                    text(targets[IP].SHARE_INFO[2][x])

                            # Local INFO
                            self.result2html_dbg.debug("Formatting Local")
                            if targets[IP].LOCAL_USERS and targets[IP].LOCAL_GROUPS:
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

                            # PASSWD_POLICY
                            self.result2html_dbg.debug("Formatting Password Policy")
                            if targets[IP].PASSWD_POLICY:
                                with tag("h4"):
                                    text("%s Password Policy" % IP)
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Flag Name")
                                            with tag('th'):
                                                text("Policy Flag Desc")
                                            with tag('th'):
                                                text("State")
                                    with tag('tbody'):
                                        for x in range(len(targets[IP].PASSWD_POLICY)):
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(password_policy_items[x][1])
                                                with tag('td'):
                                                    text(password_policy_items[x][0])
                                                with tag('td'):
                                                    text(str(targets[IP].PASSWD_POLICY[x]))

                            # PRINTER_INFO
                            self.result2html_dbg.debug("Formatting Printer Info")
                            if targets[IP].PRINTER_INFO:
                                with tag('table', klass="table table-condensed"):
                                    # Table headings
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th'):
                                                text("Printer Info")
                                    with tag('tbody'):
                                        with tag('tr'):
                                            with tag('td'):
                                                text("Not currently implemented :(")

                            # PORTS
                            self.result2html_dbg.debug("Formatting Ports")
                            if targets[IP].PORTS:
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
                                        for this_port in targets[IP].PORTS:
                                            with tag('tr'):
                                                port, service, version, state = this_port
                                                with tag('td'):
                                                    text(port)
                                                with tag('td'):
                                                    text(service)
                                                with tag('td'):
                                                    text(version)
                                                with tag('td'):
                                                    text(state)

        self.result2html_dbg.debug("Html generation success", color=Format.color_success)
        return doc.getvalue()
