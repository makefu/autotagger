#!/usr/bin/env python

#file_match=[r'.mkv$']


from . import registry

def match_empty(filename):
    # applies 'empty' tag to empty files
    tags = set()
    tags.add('empty')
    return tags

def match_nonexisting(filename):
    tags = set()
    tags.add('poor-bastard')
    return tags

# does not work with current mimetypes library we are using
#registry.register_mime('inode/x-empty',match_empty)
registry.register_regex('this-file-does-not-exist$',match_nonexisting)
