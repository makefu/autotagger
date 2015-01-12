#!/usr/bin/env python
from . import registry
import logging
from os.path import splitext,exists,dirname
import xml.etree.ElementTree as ET

show_nfo_file='tvshow.nfo'
info_ext='nfo'
log=logging.getLogger(__name__)

def match_single_nfo(nfo_file):
    tags = set()
    nfo = ET.parse(nfo_file)
    root = nfo.getroot()
    if not root.tag == 'episodedetails': raise AttributeError('file is no episodedetails file')
    
    # TODO fix all these try catch blocks, maybe they are not even needed
    try: tags.add(root.find('showtitle').text) 
    except: pass

    try: tags.add('season={}'.format(root.find('season').text)) 
    except: pass


    try: tags.add('episode={}'.format(root.find('episode').text))
    except: pass
    try: tags.add('imdb={}'.format(root.find('rating').text))
    except: pass
    return tags

def match_show_nfo(show_nfo):
    tags= set()
    nfo = ET.parse(show_nfo)
    root = nfo.getroot()
    if not root.tag == 'tvshow': raise AttributeError('file is no tvshow file')

    # breaks if None is returned
    tags.add(root.find('title').text)
    

    try: tags.add("studio_{}".format(root.find('studio').text))
    except: pass

    try: 
        for i in root.find('genre').text.split('/'):
            i = i.strip()
            tags.add(i)
    except: pass
    return tags

def match_nfo_file(f):
    log.debug('calling nfo-file-info for {}'.format(f))
    tags = set()
    try: 
        tags.update(match_single_nfo(f))
        tags.add('xbmc-metadata')
        tags.add('xbmc-tvshow-meta')
        
    except:
        pass

    try: 
        tags.update(match_show_nfo(f))
        tags.add('xbmc-metadata')
        tags.add('xbmc-episode-meta')
    except:
        pass
    return tags

def match_all(f):
    tags=set()
    log.debug('calling nfo-info for {}'.format(f))
    fname,ext = splitext(f)
    nfo_file='.'.join((fname,info_ext))
    show_nfo="/".join((dirname(f),show_nfo_file))
    if exists(nfo_file):
        log.info('found nfo for {}'.format(f))
        tags.update(match_single_nfo(nfo_file))
    if exists(show_nfo):
        log.debug('found tvshow in folder')
        tags.update(match_show_nfo(show_nfo))
    log.debug(tags)
    return tags

registry.register_mime('video/x-msvideo',match_all)
registry.register_mime('video/x-matroska',match_all)
# match  the xbmc info for single file and nfo
registry.register_regex(r'\.nfo$',match_nfo_file)
