#!/usr/bin/env python
from . import registry
import logging
from pymediainfo import MediaInfo

log=logging.getLogger(__name__)

def match_all(f):
    tags=set()
    log.debug('calling guessit for {}'.format(f))
    media_info = MediaInfo.parse(f)
    for track in media_info.tracks:
        if track.track_type == 'General':
            tags.add(track.codecs_video)
            tags.add(track.format.lower())
            tags.add("duration={}".format(track.duration//100))
        if track.track_type == 'Video':
            tags.add("{}x{}".format(track.width,track.height))
        
    # directly add the given keys to our new tag set
    # other is a list of additional tags like 'complete' or 'dualaudio'
    return tags
        

registry.register_mime('video/x-msvideo',match_all)
