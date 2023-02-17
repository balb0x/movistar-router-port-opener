class PortMessage:
    UDP = "2"
    TCP = "1"
    BOTH = "0"

    def __init__(self, title, protocol, destination, port=None, external_port_range=None, internal_port_range=None):
        self.protocol = protocol
        self.title = title
        self.destination = destination

        self.e_start = None
        self. e_end = None
        self.i_start = None
        self.i_end = None

        if port is not None:
            self.e_start = port
            self.e_end = port
            self.i_start = port
            self.i_end = port
        else:
            if external_port_range is not None and internal_port_range is None:
                self.e_start = external_port_range[0]
                self.e_end = external_port_range[1]
                self.i_start = external_port_range[0]
                self.i_end = external_port_range[1]
            elif external_port_range is None and internal_port_range is not None:
                self.e_start = internal_port_range[0]
                self.e_end = internal_port_range[1]
                self.i_start = internal_port_range[0]
                self.i_end = internal_port_range[1]
            elif external_port_range is not None and internal_port_range is not None:
                self.e_start = external_port_range[0]
                self.e_end = external_port_range[1]
                self.i_start = internal_port_range[0]
                self.i_end = internal_port_range[1]
            else:
                print("Bad configuration")

    def compose(self):
        return self.destination + "|" + str(self.e_start) + "|" + str(self.e_end) + "|" + \
           self.reverse_protocol(self.protocol) + "|" + str(self.i_start) + "|" + str(self.i_end)

    @staticmethod
    def resolve_protocol(protocol):
        if protocol == "TCP":
            return PortMessage.TCP
        elif protocol == "UDP":
            return PortMessage.UDP
        else:
            return PortMessage.BOTH

    @staticmethod
    def reverse_protocol(protocol):
        if protocol == PortMessage.TCP:
            return "TCP"
        elif protocol == PortMessage.UDP:
            return "UDP"
        else:
            return "TCP or UDP"
