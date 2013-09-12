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

import subprocess as sp
import os

# The directory of the platform's pom.xml
PLATFORM_DIR = "/home/d2shack/hackathon2/git/d2s-tools/d2s-platform"

def applicable(mimetype):
    '''
      Return a list of descriptors of workflows. Each entry is a triple of the 
      form: (identifier, human-readable name, description)
    '''
    
    return [('test1', 'Test workflow 1', 'This workflows tests something')]

def run(identifier, location, datafile):
    '''
      Starts a workflow in a separate process. If there is already a workflow
      running in the given location, the function throws an exception
      
      identifier: the string identifier for the workflow to run
      location: where to output the results of the workflow
      dataFile: which file to run the workflow on 
    ''' 
    # Read the workflow file into a string
    workflowFile = open('./'+identifier+'.yaml', 'r')
    workflowYAML = workflowFile.read()
    
    # Insert the filename
    workflowYAML.format(datafile)
    
    # Write the workflow file to the location
    wfFileOut = open(location+'/workflow.yaml', 'w')
    wfFileOut.write(workflowYAML)
    wfFileOut.close()
    
    # Change directory to the platform dir
    myDirectory = os.getcwd() # remember our original working directory
    os.chdir(PLATFORM_DIR)
    
    # Call the platform
    args = ["mvn", "exec:java", "-Dexec:mainClass='org.data2semantics.platform.run.Run'", "-Dexec:args='--output {0} {0}/workflow.yaml'".format(location)]
    sp.Popen(args) # run in the background
    
    os.chdir(myDirectory)
    
    
def status(location):
    '''
      Returns the current status of a workflow runnning in the given location 
      (a directory). The status is represented by one of the strings 
          'running'
          'no workflow'
          'error'
          'finished'
    '''
    if os.path.exists(location  + '/status.running'):
        return 'running'
    if os.path.exists(location  + '/status.finished'):
        return 'finished'
    return 'no workflow' 

