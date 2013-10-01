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



def run(workflow, datafile, location):
    '''
      Starts a workflow in a separate process. If there is already a workflow
      running in the given location, the function throws an exception
      
      identifier: the string identifier for the workflow to run
      location: where to output the results of the workflow
      dataFile: which file to run the workflow on 
    '''
    
    identifier = workflow['id']
    basedir = workflow['basedir']
    
    print "Running workflow '{}'".format(identifier)

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    if not os.path.exists(location):
        os.makedirs(location)
        
        
    workflowFileName = './'+identifier+'.yaml'
    
    if not os.path.exists(workflowFileName) :
            print "Workflow specification file '{}' does not exist".format(workflowFileName)
            return False
    
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
    
    try:
        sp.Popen(args, cwd=basedir, stdout = logFileOut, stderr = logFileOut) # run in the background
    except OSError as e:
        print "OSError: ",
        print e
        return False

    return True
    
    
 

