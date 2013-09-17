from repository import Repository
import sh

class GitRepository(Repository):
    
    
    
    def initialize(self, url):
        if not url:
            raise Exception("GitHub URL not specified")
        
        self.url = url
        
        git = sh.git.bak(_cwd=self.path)
        
        try:
            git.clone(url,_cwd=self.path)
        except Exception:
            print "Git repository was already cloned, should pull a new version, but will skip that for now"
            # git.pull(clone_url,_cwd=path)
            
        self.initialized = True
        
    def browse(self, relative_path):
        
        absolute_path = os.path.join(basedir,relative_path)
        
        files = glob("{}/*".format(absolute_path))
    
        filelist = []
        for p in files:
            (pth, fn) = os.path.split(p)
            
            mimetype = magic.from_file(p, mime=True)
            
            if os.path.isdir(p) :
                filetype = 'dir'
            else :
                filetype = 'file'
            
            print fn, mimetype
            
            relative_p = os.path.relpath(p, basedir)
            
            filelist.append({'name': fn, 'path': relative_p, 'mimetype': mimetype, 'type': filetype})
            
        
        absolute_parent = os.path.abspath(os.path.join(absolute_path, os.pardir))
        relative_parent = os.path.relpath(absolute_parent,basedir)
        
        return filelist, relative_parent
    
    
        
    