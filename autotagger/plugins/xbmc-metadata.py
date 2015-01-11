#!/usr/bin/env python
from . import registry
import logging
from os.path import splitext,exists,dirname
import xml.etree.ElementTree as ET

show_nfo_file='tvshow.nfo'
info_ext='nfo'
log=logging.getLogger(__name__)

def match_all(f):
    tags=set()
    log.debug('calling nfo-info for {}'.format(f))
    fname,ext = splitext(f)
    nfo_file='.'.join((fname,info_ext))
    show_nfo="/".join((dirname(f),show_nfo_file))
    if exists(nfo_file):
        log.info('found nfo for {}'.format(f))
        nfo = ET.parse(nfo_file)
        root = nfo.getroot()
        # TODO fix all these try catch blocks
        try: tags.add('season={}'.format(root.find('season').text)) 
        except: pass
        try: tags.add('episode={}'.format(root.find('episode').text))
        except: pass
        try: tags.add('imdb={}'.format(root.find('rating').text))
        except: pass
    if exists(show_nfo):
        log.debug('found tvshow in folder')
        nfo = ET.parse(show_nfo)
        root = nfo.getroot()

        try: tags.add(root.find('title').text)
        except: pass
        try: tags.add("studio_{}".format(root.find('studio').text))
        except: pass
        try: 
            for i in root.find('genre').text.split('/'):
                i = i.strip()
                tags.add(i)
        except: pass
    log.debug(tags)            
    return tags
        

registry.register_mime('video/x-msvideo',match_all)
registry.register_mime('video/x-matroska',match_all)
