import os
from app import SCRATCH
import sh
import os
from glob import glob
import magic

class Dataset(object):
    
    BASEDIR = SCRATCH
    
    basdir = ""
    name = ""
    initialized = False
    
    def __init__(self, name, basedir = BASEDIR):
        self.basedir = basedir
        self.name = name     
        
        if not(os.path.exists(basedir)):
            raise Exception("Basedir {} does not exist!".format(basedir))
        
        self.path = os.path.join(basedir, name)
        
        if os.path.exists(self.path):
            self.initialized = True
                
    
    def browse(self, path = None):
        pass
    

    
    
    


class GitDataset(Dataset):
    
    
    
    def initialize(self, url):
        if self.initialized :
            print "Already initialized!"
            return
            
        if not url:
            raise Exception("GitHub URL not specified")
        
        self.url = url
        
        git = sh.git.bake(_cwd=self.basedir)
        
        try:
            git.clone(url,_cwd=self.basedir)
        except Exception as e:
            print e
            print "Git repository was already cloned, should pull a new version, but will skip that for now"
            # git.pull(clone_url,_cwd=path)
            
        self.initialized = True
        
    def browse(self, relative_path):
        
        absolute_path = os.path.join(self.basedir,relative_path)
        
        files = glob("{}/*".format(absolute_path))
    
        filelist = []
        for p in files:
            (pth, fn) = os.path.split(p)
            
            mimetype = magic.from_file(p, mime=True)
            
            if mimetype == "text/plain" and fn[-3:] == "ttl" :
                mimetype = "text/turtle"    
            
            if os.path.isdir(p) :
                filetype = 'dir'
            else :
                filetype = 'file'
            
            
            relative_p = os.path.relpath(p, self.basedir)
            
            filelist.append({'name': fn, 'path': relative_p, 'mimetype': mimetype, 'type': filetype})
        
        
        absolute_parent = os.path.abspath(os.path.join(absolute_path, os.pardir))
        relative_parent = os.path.relpath(absolute_parent,self.basedir)
        
        if absolute_parent == os.path.dirname(self.path) or '..' in relative_parent or relative_parent == '.' :
            print absolute_parent, relative_parent
            relative_parent = ''
        
        
        return filelist, relative_parent