
try:
    #py3
    from urllib.request import pathname2url
except:
    #py2
    from urllib import pathname2url

import mimetypes
import logging

log = logging.getLogger('parser')

def get_mimetype(f):
    url = pathname2url(f)
    return mimetypes.guess_type(url)[0]

def match_mime(f):
    mime = get_mimetype(f)


def match_regex(f):
    raise NotImplementedError('regex matching not implemented')
