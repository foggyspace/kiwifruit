class ScannerTopException(Exception):
    pass


class DestinationUnReachable(ScannerTopException):
    def __init__(self,dest):
        self.args = dest
        self.dest = dest
