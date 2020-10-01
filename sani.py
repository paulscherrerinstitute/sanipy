#!/usr/bin/env python


def main():
    clargs = handle_clargs()
    from commands import run
    run(clargs)


def handle_clargs():
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="valid commands")

    parser_check = subparsers.add_parser("check", help="check a list of channels", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_check.add_argument("filename", help="name of input channel-list file")
    parser_check.add_argument("-o", "--output", help="output CSV file", default=None)
    parser_check.add_argument("-q", "--quiet", help="do not show each channel's answer", action="store_true")
    parser_check.add_argument("-s", "--serial", help="do not run checks in parallel", action="store_true")
    parser_check.add_argument("-t", "--timeout", help="connection timeout in seconds", type=float, default=1)

    parser_compare = subparsers.add_parser("compare", help="compare two check results")
    parser_compare.add_argument("filenames", metavar="filename", nargs=2, help="name of input CSV file, two are needed")
    parser_compare.add_argument("-v", "--ignore-values", help="do not check values", action="store_true")

    clargs = parser.parse_args()

    if not clargs.command:
        parser.print_help()
        raise SystemExit

    return clargs



if __name__ == "__main__":
    main()



