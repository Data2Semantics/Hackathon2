import os
from app import SCRATCH
import sh
import os
from glob import glob
import magic


URL_FILE = '.d2s.url'
TYPE_FILE = '.d2s.type'
BASEDIR = SCRATCH

class Dataset(object):
    
    
    def __init__(self, name, basedir = BASEDIR):
        self.basedir = basedir
        self.name = name
        self.initialized = False
        
        if not(os.path.exists(basedir)):
            raise Exception("Basedir {} does not exist!".format(basedir))
        
        self.path = os.path.join(basedir, name)
        
        type_path = os.path.join(self.path,TYPE_FILE)
        
        if os.path.exists(self.path) and os.path.exists(type_path):
            type_file = open(type_path,'r')
            self.type = type_file.read()
            type_file.close()
            
            self.initialized = True
                
    
    def browse(self, path = None):
        pass
    

    
    
    


class GitDataset(Dataset):
    
    def __init__(self, name, basedir = BASEDIR):
        Dataset.__init__(self, name, basedir)
        
        clone_url_path = os.path.join(self.path, URL_FILE)
        
        if os.path.exists(clone_url_path):
            clone_url_file = open(clone_url_path, 'r')
            self.url = clone_url_file.read();
            clone_url_file.close()
        else :
            # If no clone URL is specified, the dataset is not yet initialized
            self.initialized = False
    
    
    
    def initialize(self, url):
        if self.initialized :
            print "Already initialized!"
            return
            
        if not url:
            raise Exception("GitHub URL not specified")
        
        self.url = url
        self.type = "util.dataset.GitDataset"
        
        git = sh.git.bake(_cwd=self.basedir)
        
        try:
            git.clone(url,_cwd=self.basedir)
            
            clone_url_path = os.path.join(self.path, URL_FILE)
            clone_url_file = open(clone_url_path, 'w')
            clone_url_file.write(self.url)
            clone_url_file.close()
            
            
            type_path = os.path.join(self.path, TYPE_FILE)
            type_file = open(type_path, 'w')
            type_file.write(self.type)
            type_file.close()
        except Exception as e:
            print e
            print "Git repository was already cloned, should pull a new version, but will skip that for now"
            # git.pull(clone_url,_cwd=path)
            
        self.initialized = True
        
        
        
    def browse(self, relative_path):
        if not self.initialized :
            raise Exception('Dataset must be initialized first!')
        
        absolute_path = os.path.join(self.basedir,relative_path)
        
        files = glob("{}/*".format(absolute_path))
    
        filelist = []
        for p in files:
            (pth, fn) = os.path.split(p)
            
            mimetype = magic.from_file(p, mime=True)
            
            if mimetype == "text/plain" and (fn[-3:] == "ttl" or fn[-2:] == 'n3') :
                mimetype = "text/turtle"
            if mimetype == "text/plain" and (fn[-3:] == "owl" or fn[-2:] == 'rdf') :
                mimetype = "application/rdf+xml"
            
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