#!/usr/bin/env python3
import logging
log=logging.getLogger(__name__)
_mime_registry=[]
_regex_registry=[]
import re

def register_mime(mimetype,function):
    log.debug('registered {} for mime {}'.format(mimetype,function))
    _mime_registry.append((mimetype,function))

def register_regex(regex,function):
    _regex_registry.append((re.compile(regex),function))

def funcs_for_mime(mimetype):
    for mime,f in _mime_registry:
        if mimetype == mime:
            yield f

def funcs_for_mime(mimetype):
    for mime,f in _mime_registry:
        if mimetype == mime:
            yield f
def funcs_for_regex(filename):
    for regex,f in _regex_registry:
        if regex.search(filename):
            yield f
