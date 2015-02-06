import logging
from os import mkdir
from os.path import isdir, join
from mythtvlib.settings import settings

logger = logging.getLogger(__name__)

class MythTVUtilsException(Exception):
    pass

def get_tmp_dir():
    "Answer the location used for temporary and cache files"
    tmp_dir = None
    for d in settings.TMP_DIRS:
        if not isdir(d):
            break
        tmp_dir = join(d, 'MythTV_CLI')
        if not isdir(tmp_dir):
            mkdir(tmp_dir)
        break
    if tmp_dir is None:
        msg = "Unable to find tmp directory"
        logger.error(msg)
        raise MythTVUtilsException(msg)
    logger.debug("got tmp dir = {0}".format(tmp_dir))
    return tmp_dir
