#!/usr/bin/env python3

import argparse
#import logging
import logging.config
import sys
from os.path import isdir, abspath, dirname, realpath, join, basename
from urllib.error import URLError


# Try and ensure imports will work in development workspace
mydir = dirname(realpath(__file__))
proposed_path = abspath(join(mydir, '..'))
if isdir(join(proposed_path, 'mythtvlib')) and (proposed_path not in sys.path):
    sys.path.append(proposed_path)

from mythtvlib import __VERSION__
from mythtvlib.backend import MythTVBackend
from mythtvlib.object import MythTVQuerySet

from mythtvlib.settings import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(basename(sys.argv[0]))


class MythTVCLIException(Exception):
    pass



def update(args):
    # update <class name> <filter field> <filter regex> <update field> <update value>
    if len(args.params) != 5:
        msg = "Expect 5 parameters, got {0}".format(len(args.params))
        logger.fatal(msg)
        exit(1)
    class_name = "MythTV" + args.params[0]
    filter_field = args.params[1]
    filter_regex = args.params[2]
    update_field = args.params[3]
    update_value = args.params[4]
    update_class = MythTVQuerySet(class_name)
    if update_class is None:
        msg = "Unknown class name: {0}".format(class_name)
        logger.fata(msg)
        exit(1)
    logger.info("update {klass} {ffield} '{fregex}' {ufield} '{uvalue}'".format(
        klass=args.params[0],
        ffield=filter_field,
        fregex=filter_regex,
        ufield=update_field,
        uvalue=update_value))
    kwargs = {filter_field : filter_regex}
    update_class = update_class.filter(**kwargs)
    update_records = update_class.all()
    if len(update_records) == 0:
        logger.info("Nothing to update")
        return
    fmt_string = "{obj} {field}: '{old}' => '{new}'"
    if not args.yes:
        for rec in update_records:
            print(fmt_string.format(
                obj=str(rec),
                field=update_field,
                old=getattr(rec, update_field),
                new=update_value))
        proceed = input("Proceed with update? [y/N] ")
        if proceed.lower() not in ['y', 'yes']:
            logger.info("User aborted update")
            return
    fmt_string = "Updated: {obj} {field}: '{old}' => '{new}'"
    for rec in update_records:
        setattr(rec, update_field, update_value)
        rec.save()
        logger.info(fmt_string.format(
            obj=str(rec),
            field=update_field,
            old=getattr(rec, update_field),
            new=update_value))
    logger.info("Updated {0} record(s)".format(len(update_records)))
    return



def main():
    logger.debug("Starting")
    services_string = ", ".join(MythTVBackend.services())
    epilog = """
{prog} has 2 basic use cases:

    {prog} dump <service> <operation> <key...>
        Print the results of the requested service/operation
    {prog} update <class name> <filter field> <filter regex> <update field> <update value>
        Update the records matching the supplied regular expression in the
        requested class.

Valid Services: {services}

Valid Class Names: Channel

Additional Help:

   {prog} dump <service> help # for help on individual services.
   {prog} dump <service> <operation> help # for detailed parameter information

    
MythTV Web Services Documentation: https://www.mythtv.org/wiki/Services_API
""".format(
            services=services_string,
            prog=basename(sys.argv[0]))
    parser = argparse.ArgumentParser(description="MythTV Web Services CLI",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('command',
                        choices=['dump', 'update'],
                        help="Maintenance command, see below")
    parser.add_argument('params',
                        nargs='+',
                        help="Command parameter(s)")
    parser.add_argument('--post', action='store_true',
                        default=False,
                        help='Show POST operations with operation help')
    parser.add_argument('--hostname',
                        default=None,
                        help='MythTV Backend hostname')
    parser.add_argument('--server-port', dest='port',
                        default=None,
                        help="MythTV Backend services port")
    parser.add_argument('-y', action='store_true',
                        dest='yes',
                        default=False,
                        help="Execute updates without user confirmation")
    parser.add_argument('--version',
                        action='version',version='%(prog)s version '+ __VERSION__)
    args = parser.parse_args()

    backend = MythTVBackend.default(hostname=args.hostname, port=args.port)
    if args.command == 'dump':
        try:
            service = backend.service_api(args.params[0])
        except (ConnectionRefusedError, URLError) as e:
            if backend.hostname == "localhost":
                logger.info("hostname=='localhost' - has it been set in mythtv_cli_settings?")
            msg = ("Unable to get backend service.  Please check "
                   "hostname={host}, port={port} is correct and the backend "
                   "is up").format(
                        host=backend.hostname, port=backend.port)
            logger.fatal(msg)
            logger.fatal("Error: {0}".format(e))
            exit(1)
        # TODO: MythTVServiceAPI can return the help and 
        #       process the command like any other
        if args.params[1] == 'help':
            service.print_help(show_post=args.post)
        else:
            resp = service.execute_args(args.params[1:])
            print(resp)
    elif args.command == 'update':
        update(args)
    else:
        # argparse should catch this before we get here
        raise MythTVCLIException("Unknown command: {0}".format(args.command))
    logger.debug("Done")
    return



if __name__ == "__main__":
    main()
