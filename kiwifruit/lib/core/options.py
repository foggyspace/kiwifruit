import sys

from argparse import ArgumentParser, ArgumentError

from kiwifruit.lib.core.data import commandline_options


def parse_commandline():
    add_commandline_options = ArgumentParser()
    add_commandline_options.add_argument("-t", "--task", action="store", dest="task", help="task id")
    add_commandline_options.add_argument("-u", "--url", action="store", dest="url", help="target url")
    add_commandline_options.add_argument("-b", "--base", action="store", dest="base", default="/", help="the base directory of the domain")
    add_commandline_options.add_argument("-d", "--depth", action="store", dest="depth", default=0, help="crawler depth", type=int)
    add_commandline_options.add_argument("-c", "--count", action="store", dest="count", default=0, help="crawler url max count", type=int)
    add_commandline_options.add_argument("--cookie", action="store", dest="cookie", help="http cookie header")
    add_commandline_options.add_argument("--connect-timeout", action="store", dest="connect timeout", help="set connect timeout")
    add_commandline_options.add_argument("--timeout", action="store", dest="timeout", help="network timeout")
    add_commandline_options.add_argument("--continue", dest="continue", action="store_true", help="task continue run")
    try:
        args = add_commandline_options.parse_args(sys.argv[1:])
        commandline_options.update(args.__dict__)
        print(commandline_options)
    except ArgumentError:
        print(add_commandline_options.error())