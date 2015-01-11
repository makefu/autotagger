#!/usr/bin/env python
from . import registry
import logging

from guessit import guess_file_info
import pdb
log=logging.getLogger(__name__)

def match_all(f):
    tags=set()
    log.debug('calling guessit for {}'.format(f))
    ret = guess_file_info(f)

    # directly add the given keys to our new tag set
    for i in ('videoCodec','container','format',
            'releaseGroup','audioCodec'):
        if i in ret: tags.add(ret[i])
    
    for i in ('season','episode','year'):
        if i in ret: tags.add("{}={}".format(i,ret[i]))

    # other is a list of additional tags like 'complete' or 'dualaudio'
    if 'other' in ret: tags.update(ret['other'])

    return tags
        

registry.register_mime('video/x-matroska',match_all)
registry.register_mime('video/x-msvideo',match_all)
