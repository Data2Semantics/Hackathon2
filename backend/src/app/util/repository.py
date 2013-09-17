import os


class Repository(object):
    
    BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch')
    
    basdir, name = ""
    initialized = False
    
    def __init__(self, name, basedir = BASEDIR):
        self.basedir = basedir
        self.name = name     
        
        if not(os.path.exists(basedir)):
            raise Exception("Basedir {} does not exist!".format(basedir))
        
        self.path = os.path.join(basedir, name)
                
    
    def browse(self, path = None):
        pass
    

    
    
    