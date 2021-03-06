#!/usr/bin/env python


def main():
    clargs = handle_clargs()
    from commands import run_command
    run_command(clargs)


def handle_clargs():
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="valid commands")

    parser_check = subparsers.add_parser("check", help="check a list of channels", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_check.add_argument("filename", help="name of input channel-list file")
    parser_check.add_argument("-o", "--output", help="output CSV file")
    parser_check.add_argument("-q", "--quiet", help="do not show each channel's answer", action="store_true")
    parser_check.add_argument("-s", "--serial", help="do not run checks in parallel", action="store_true")
    parser_check.add_argument("-t", "--timeout", help="connection timeout in seconds", type=float, default=1)

    parser_compare = subparsers.add_parser("compare", help="compare two check results")
    parser_compare.add_argument("filenames", metavar="filename", nargs=2, help="name of input CSV file, two are needed")
    parser_compare.add_argument("-v", "--ignore-values", help="do not check values", action="store_true")

    parser_goto = subparsers.add_parser("goto", help="go to stored values")
    parser_goto.add_argument("filename", help="name of input CSV file")
    parser_goto.add_argument("-a", "--ignore-alarm", help="do not put into PVs that were in an alarm state during check", action="store_true")
    parser_goto.add_argument("-q", "--quiet", help="do not show each channel's answer", action="store_true")
    parser_goto.add_argument("-s", "--serial", help="do not run checks in parallel", action="store_true")
    parser_goto.add_argument("-t", "--timeout", help="connection and put completion timeout in seconds", type=float, default=1)

    clargs = parser.parse_args()

    if not clargs.command:
        parser.print_help()
        raise SystemExit

    return clargs



if __name__ == "__main__":
    main()



