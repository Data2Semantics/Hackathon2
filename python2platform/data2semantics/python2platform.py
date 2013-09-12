'''
This module provides an API frontend for the platform. It provides the following
functionality:
 - Return a list of applicable workflows for a given filetype
   - Each workflow is identified by a unique string
 - Start a workflow in a given location, for a given dataset
   
The expected procedure is something like this:
- User chooses a datafile 
- Check for applicable workflows, offer to user [applicable/1]
- User chooses a workflow 
- Prepare a directory where the workflow will run 
- Run the chosen workflow in that directory [run/3]

- Check whether the workflow is finished [status/1] 

@author: Peter
'''

def applicable(mimetype):
    '''
      Return a list of descriptors of workflows. Each entry is a triple of the 
      form: (identifier, human-readable name, description)
    '''
    return [
        ('test1', 'Test workflow 1', 'This workflows tests something') 
        ('test2', 'Test workflow 2', 'This workflow does another thing')
    ]

def run(workflow_identifier, location, data):
    '''
      Starts a workflow in a separate process. If there is already a workflow
      running in the given location, the function throws an exception
    ''' 
    
def status(location):
    '''
      Returns the current status of a workflow runnning in the given location 
      (a directory). The status is represented by one of the strings 
          'running'
          'no workflow found'
          'error'
          'finished'
    '''
    
