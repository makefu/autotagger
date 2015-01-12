# python autotagger core functionality

try:
    #py3
    from urllib.request import pathname2url
except:
    #py2
    from urllib import pathname2url

from taggers import TMSU
import mimetypes
import logging
log = logging.getLogger(__name__)

def set_lol_from_str(lol):
  numeric_level = getattr(logging,lol.upper(),None)
  if not isinstance(numeric_level,int):
    raise AttributeError('No such log level {}'.format(lol))
  logging.basicConfig(level=numeric_level)
  log.setLevel(numeric_level)

def get_tagger(ts):
    ts = ts.lower()
    if ts == 'tmsu':
        return TMSU()
    else:
        raise AttributeError('No such tagger {}'.format(ts))




def get_mimetype(f):
    url = pathname2url(f)
    return mimetypes.guess_type(url)[0]

def match_mime(f):
    mime = get_mimetype(f)

def match_regex(f):
    raise NotImplementedError('regex matching not implemented')
