import sys
import getopt
from parseconf import call

if __name__ == '__main__':
    command = "all"
    location = ""

    try:
        options, args = getopt.getopt(sys.argv[1:], "f:l:")
    except getopt.GetoptError:
        sys.exit()
    for name, value in options:
        if name == "-f":
            command = value
        elif name == "-l":
            location = value

    call(command, location)
