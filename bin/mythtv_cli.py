#!/usr/bin/env python3

import argparse
import sys
from os.path import isdir, abspath, dirname, realpath, join, basename

# Try and ensure imports will work in development workspace
mydir = dirname(realpath(__file__))
proposed_path = abspath(join(mydir, '..'))
if isdir(join(proposed_path, 'mythtvlib')) and (proposed_path not in sys.path):
    sys.path.append(proposed_path)

from mythtvlib.services import MythTVService

def main():
    services_string = ", ".join(MythTVService.services)
    epilog = """
Valid Services: {services}
    
Additional Help:

   {prog} <service> help # for help on individual services.
   {prog} <service> <operation> help # for detailed parameter information
    
Documentation: https://www.mythtv.org/wiki/Services_API
""".format(
            services=services_string,
            prog=basename(sys.argv[0]))
    parser = argparse.ArgumentParser(description="MythTV Web Services CLI",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('service',
                        help='MythTV Service Name')
    parser.add_argument('operation',
                        nargs='+',
                        help='MythTV Service Operation and parameters')
    parser.add_argument('--post', action='store_true',
                        default=False,
                        help='Show POST operations with operation help')
    args = parser.parse_args()

    service = MythTVService(args.service)
    if args.operation[0] == 'help':
        service.print_help(show_post=args.post)
    else:
        resp = service.execute_args(args)
        print(resp)

if __name__ == "__main__":
    main()
