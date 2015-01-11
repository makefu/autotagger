#!/usr/bin/python

import logging
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

from parser import get_mimetype

from plugins import registry
# load all plugins
from plugins import *
from taggers import TMSU
import sys

log = logging.getLogger(__name__)

if __name__ == '__main__':
    f=sys.argv[1]
    tagger = TMSU()
    mime = get_mimetype(f)
    log.info('mimetype for {} is: {}'.format(f,mime))
    tags=set()
    for func in registry.funcs_for_mime(mime):
        tags.update(func(f))
        log.info("{} => {}".format(func,tags))
    log.info("adding {} to file {}".format(tags,f))
    tagger.tag(f,tags)
