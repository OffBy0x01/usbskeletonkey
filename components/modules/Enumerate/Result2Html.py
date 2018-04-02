from yattag import Doc, indent


def generate_output(targets):
    """
    Description:
                Converts Enumerate output to human-readable form

    :param targets:     List containing TargetInfo Objects
    :return:            Bootstrap-based HTML5 page of results
    """

    doc, tag, text = Doc().tagtext()
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
                    for IP in targets.keys():

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

    return indent(doc.getvalue())