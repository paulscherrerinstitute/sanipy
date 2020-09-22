import logging as log


LEVELS = (
#    log.CRITICAL,
    log.ERROR,
    log.WARNING,
    log.INFO,
    log.DEBUG,
    log.NOTSET
)


def set_log_level(verbosity):
    ntotal = len(LEVELS) - 1
    index = min(verbosity, ntotal)
    level = LEVELS[index]
    log.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")





#from logger import log, set_log_level

#set_log_level(clargs.verbose)
