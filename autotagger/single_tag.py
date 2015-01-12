#!/usr/bin/python
""" Tag single files
Usage: single_tag [-t TAGGER [--db DATABASE]] [-l LOGLEVEL] <file>...

Options:
    -t TAGGER       The tagger to be used [default: tmsu]
    -l LOGLEVEL     The loglevel [default: info]
                    may be: debug,info,warn,error
    --db DATABASE   path the tagger database (if applicable)
    
TODO:   this file may be come obsolete and be replaced by an universal tag tool
        with recuse and single mode.
"""


import logging
#logging.basicConfig(level=logging.INFO)

from core import get_mimetype,set_lol_from_str,get_tagger

from plugins import registry
# load all plugins
from plugins import *
import sys
from docopt import docopt
log = logging.getLogger('main')

if __name__ == '__main__':
    args = docopt(__doc__)

    set_lol_from_str(args['-l'])
    tagger = get_tagger(args['-t'],args['--db'])
    for f in args['<file>']:
        mime = get_mimetype(f)
        log.debug('mimetype for {} is: {}'.format(f,mime))
        tags=set()
        for func in registry.funcs_for_mime(mime):
            tags.update(func(f))
            log.info("{} => {}".format(func,tags))
        for func in registry.funcs_for_regex(f):
            tags.update(func(f))
            log.info("{} => {}".format(func,tags))

        log.info("adding {} to file {}".format(tags,f))
        tagger.tag(f,tags)
