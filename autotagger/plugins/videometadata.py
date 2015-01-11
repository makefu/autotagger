#!/usr/bin/env python
from . import registry
import logging

import enzyme
import pdb
log=logging.getLogger(__name__)

def match_matroska(f):
    tags=set()
    log.debug('calling matroska for {}'.format(f))
    with open(f,'rb') as fo:
        data = enzyme.MKV(fo)
        log.debug(data)

        duration = int(data.info.duration.total_seconds())
        tags.add('duration={}'.format(duration))
        for v in data.video_tracks:
            tags.add("{}x{}".format(v.width,v.height))
            #tags.add("{}p".format(v.height))
            # the language of the video stream, maybe not that interesting
            #tag.add("{}_video".format(v.language))
            # the codec used
            #tag.add(v.codec_id)

            # if the mkv has a video track it is a video
            tags.add("video")

        if not "video" in tags: tags.add("audio")

        for a in data.audio_tracks:
            # we use audio language as main language
            lang = a.language
            if not lang or lang is 'unk': lang='unk_lang'
            tags.add("{}_audio".format(lang))
            # we could also check for audio channels and khz used but i do not
            # find it very useful
            #tag.add("{}_channels".format(a.channels))
            #tag.add(int(a..sampling_frequency))
            # audio codec name (like AAC)
            #tag.add(data.audio_tracks[0].codec_id)

        for s in data.subtitle_tracks:
            lang = s.language
            if not lang or lang is 'unk': lang='unk_lang'
            tags.add("{}_subtitle".format(lang))


        # mkv tags are a lot more complex than ours
        #tags.update(data.tags)
        log.debug(tags)
        return tags
        

registry.register_mime('video/x-matroska',match_matroska)
