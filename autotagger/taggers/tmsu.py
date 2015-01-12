from os.path import expanduser
import logging
import subprocess

log=logging.getLogger('tmsu')
class TMSU:
    db=''
    tmsu_path='/usr/bin/tmsu'

    def __init__(self,db='~/.tmsu/default.db'):
        self.db=expanduser(db)
        log.debug('setting db to {}'.format(self.db))
    
    def cleanup_tag(self,t):
        replacement={ ' ':'_',
                      '(':'',
                      ')':'',
                      '/':''}
        for orig,new in replacement.items():
            t = t.replace(orig,new)
        return t
    def tag(self,f,tags):
        """
        f : the file to tag
        tags: list of tags to apply
        """
        if not tags:
            log.warn('no tags for file {}'.format(f))
            return

        tags = list(tags)
        # tags must not contain spaces ... and this in the year 2015 ...
        tags = [self.cleanup_tag(str(tag)) for tag in tags]
        log.debug('tagging {} with tags {}'.format(f,tags))
        cmd=[self.tmsu_path,'-D',self.db, 'tag',f]+tags
        log.debug('running {}'.format(' '.join(cmd)))
        ret = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #ret = subprocess.Popen(cmd)
        (out,err) = ret.communicate()
        #ret = subprocess.check_output(cmd)
        log.error('stdout: {}'.format(out.decode()))
        log.error('stderr: {}'.format(err.decode()))

        if ret.returncode != 0:
            log.error('tagging failed with {}'.format(e))
            log.error('stdout: {}'.format(out))
            log.error('stderr: {}'.format(err))
        elif not out:
            log.debug('no new tags for {}'.format(f))
        else:
            log.info('new tags in db {}'.format(out.decode('utf-8')))
