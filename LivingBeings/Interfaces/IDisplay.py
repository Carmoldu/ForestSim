class PrintColors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class IDisplay:
    def display(self):
        pass


class LumberjackDisplay(IDisplay):
    def display(self):
        return PrintColors.PURPLE + "L" + PrintColors.ENDC
        #return "L"


class TreeDisplay(IDisplay):
    def display(self):
        return PrintColors.GREEN + "T" + PrintColors.ENDC
        #return "T"


class BearDisplay(IDisplay):
    def display(self):
        return PrintColors.RED + "B" + PrintColors.ENDC
        #return "B"
