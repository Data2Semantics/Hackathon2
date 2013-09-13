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

compression = {
            'run from': '/home/d2shack/hackathon2/git/d2s-tools/complexity-analysis-tools/complexity-analysis-tools', 
            'name': 'Compression', 
            'description': 'Computes the compressed and uncompressed size. The compressed size of the data servers as an upper bound for the amount of information it contains.'
        }
rdf_compression = {
            'run from': '/home/d2shack/hackathon2/git/d2s-tools/RDFmodel', 
            'name': 'RDF Compression', 
            'description': 'Computes the size of an RDF dataset under a specialized model.'
        }

uri_partition = {
            'run from': '/home/d2shack/hackathon2/git/d2s-tools/RDFmodel', 
            'name': 'URI Partitioning', 
            'description': 'Analyzes the URIs in the data and partitions them into functional units.'
        }

adjacency = {
            'run from': '/home/d2shack/hackathon2/git/d2s-tools/complexity-analysis-tools/complexity-analysis-tools', 
            'name': 'Adjacency Matrices', 
            'description': 'Creates density plots of the adjacency matrix of the data, for a variety of orderings.'
        }

extract_xls = {
            'run from': '/home/d2shack/hackathon2/git/d2s-tools/RDFmodel', 
            'name': 'Extract XLS string', 
            'description': 'Test python module extracting string from xls.'
        }


workflows = {}
workflows['compression'] = compression
workflows['rdf_compression'] = rdf_compression
workflows['uri_partition'] = uri_partition
workflows['adjacency'] = uri_partition
workflows['extract_xls'] = extract_xls
 

def applicable(mimetype):
    '''
      Return a list of descriptors of workflows. Each entry is a triple of the 
      form: (identifier, human-readable name, description)
    '''
    list = [('compression', workflows['compression']['name'], workflows['compression']['description'])]
    
    if(mimetype is 'text/turtle' or mimetype is 'application/rdf+xml'):
        list.append[('rdf_compression', workflows['rdf_compression']['name'], workflows['rdf_compression']['description'])]
        list.append[('uri_partition', workflows['uri_partition']['name'], workflows['uri_partition']['description'])]
        list.append[('adjacency', workflows['adjacency']['name'], workflows['adjacency']['description'])]

    return list

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
    
    # Call the platform
    args = ["mvn", "exec:java", "-Dexec.mainClass=org.data2semantics.platform.run.Run", '-Dexec.args=--output {0} {0}/workflow.yaml'.format(location)]
    sp.Popen(args, cwd=workflows[identifier]['run from']) # run in the background
    
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

