import os
from app import SCRATCH

class Repository(object):
    
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
    

    
    
    
