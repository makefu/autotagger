#!/usr/bin/python
""" Tag single files
Usage: recurse_tag [-t TAGGER [--db DATABASE]] [-l LOGLEVEL] <folder>

Options:
    -t TAGGER       The tagger to be used [default: tmsu]
    --db DATABASE   Path to the tagger database (if applicable)
    -l LOGLEVEL     The loglevel [default: info]
                    may be: debug,info,warn,error

"""


import logging
from core import get_mimetype,set_lol_from_str,get_tagger

from plugins import registry
# load all plugins
from plugins import *
import sys
from docopt import docopt
import os.path
from os import walk
log = logging.getLogger(__name__)

if __name__ == '__main__':
    args = docopt(__doc__)

    set_lol_from_str(args['-l'])
    tagger = get_tagger(args['-t'],args['--db'])
    for (path,dirs,files) in os.walk(args['<folder>']):
        for f in files:
            f = os.path.join(path,f)
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
