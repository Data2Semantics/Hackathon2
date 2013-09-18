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
import yaml

# The directory of the platform's pom.xml
PLATFORM_DIR = "/home/d2shack/hackathon2/git/d2s-tools/d2s-platform"

WORKFLOW_CONFIG = os.path.join(os.path.dirname(__file__),"workflows.yaml")
 
workflows = yaml.load(open(WORKFLOW_CONFIG,'r'))

def get_applicable_workflows(mimetype):
    '''
      Return a list of descriptors of workflows. Each entry is a triple of the 
      form: (identifier, human-readable name, description)
    '''

    ## Select those workflows which have the specified mimetype listed 
    applicable_workflows = [wf for wf in workflows if ('any' in wf['mimetypes'] or mimetype in wf['mimetypes'])]
    
    return applicable_workflows

def run(identifier, location, datafile):
    '''
      Starts a workflow in a separate process. If there is already a workflow
      running in the given location, the function throws an exception
      
      identifier: the string identifier for the workflow to run
      location: where to output the results of the workflow
      dataFile: which file to run the workflow on 
    '''
    
    identified_workflows = [wf for wf in workflows if wf['id'] == identifier ]
    
    if len(identified_workflows) == 0 :
        raise Exception("No matching workflows found")
    elif len(identified_workflows) > 1 :
        raise Exception("Multiple workflows with the same identifier ({})".format(identifier))
    else :
        wf = identified_workflows[0]
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    
    if not os.path.exists(location):
        os.makedirs(location)
        
    # Read the workflow file into a string
    workflowFile = open('./'+identifier+'.yaml', 'r')
    workflowYAML = workflowFile.read()
    
    # Insert the filename
    workflowYAML = workflowYAML.format(datafile)
    
    # Write the workflow file to the location
    wfFileOut = open(location+'/workflow.yaml', 'w')
    wfFileOut.write(workflowYAML)
    wfFileOut.close()
    
    logFileOut = open(location+'/workflow.log', 'w')
    # Call the platform
    args = ["mvn", "exec:java", "-Dexec.mainClass=org.data2semantics.platform.run.Run", '-Dexec.args=--output {0} {0}/workflow.yaml'.format(location)]
    

    sp.Popen(args, cwd=wf['basedir'], stdout = logFileOut, stderr = logFileOut) # run in the background
    
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
    if os.path.exists(location  + '/status.error'):
        return 'error'
    return 'no workflow' 

