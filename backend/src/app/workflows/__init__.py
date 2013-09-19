from app import app, SCRATCH
import os
import yaml
import importlib
from app.util.dataset import Dataset


WORKFLOW_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)),"workflows.yaml")
WORKFLOW_RESULTS = os.path.join(os.path.abspath(os.path.join(os.path.join(__file__,os.pardir), os.pardir)), 'results')

workflows = yaml.load(open(WORKFLOW_CONFIG,'r'))

def get_workflow_by_id(workflow_identifier):
    identified_workflows = [wf for wf in workflows if wf['id'] == workflow_identifier ]
    
    if len(identified_workflows) == 0 :
        raise Exception("No matching workflows found")
    elif len(identified_workflows) > 1 :
        raise Exception("Multiple workflows with the same identifier ({})".format(workflow_identifier))
        
    return identified_workflows[0]

def get_target(workflow_identifier, source):
    app.logger.debug("source: {}".format(source))
    app.logger.debug("WORKFLOW_RESULTS: {}".format(WORKFLOW_RESULTS))
    
    target = os.path.join(os.path.join(WORKFLOW_RESULTS,source),workflow_identifier)
    
    app.logger.debug('Using target {}'.format(target))
    return target


def import_workflow_module(module_name):
    app.logger.debug("Importing module {}".format(module_name))
    module = __import__(module_name)
    app.logger.debug("Done")
    
    return module


def run(workflow_identifier, dataset_name, source):
    """
        Run the workflow specified by the workflow_identifier, on the file at the source location
    """
    workflow = get_workflow_by_id(workflow_identifier)
    
    dataset = Dataset(dataset_name)
    
    if not dataset.initialized :
        raise Exception("Dataset {} is not yet initialized, cannot run workflow {}".format(dataset_name, workflow_identifier))
    else :
        last = dataset.type.rfind('.')
        module_name = dataset.type[:last]
        class_name = dataset.type[last+1:]
        
        app.logger.debug("Importing dataset type {} from {}".format(class_name, module_name))
        pp = __import__(module_name,[class_name])
        
        app.logger.debug("Casting dataset {} to type {}".format(dataset, dataset.type))
        dataset.__class__ = eval(dataset.type[1:])
        dataset.__init__(dataset_name)
        
    ### Tot Hier
    
    if workflow['type'] == 'file' :
        app.logger.debug("Workflow type is 'file'")
        pass
    elif workflow['type'] == dataset.type :
        app.logger.debug('Found matching workflow for {}'.format(workflow['type']))
    else :
        app.logger.debug('{} is not {}'.format(workflow['type'],type(dataset_name)))
    
    
    target = get_target(workflow_identifier, source)
    
    absolute_path_to_source = os.path.join(SCRATCH,source)
    
    module_name = workflow['module']    
    module = import_workflow_module(module_name)
    
    app.logger.debug("Type: {}".format(type(module)))
    
    app.logger.debug("Running workflow '{}' ({}) on {}. Output will be stored at {}".format(workflow_identifier,module_name,source,target))
    module.run(workflow, absolute_path_to_source, target)
    app.logger.debug("Workflow started")
    
    return
    
    
def status(workflow_identifier, source):
    '''
      Returns the current status of a workflow runnning in the given location 
      (a directory). The status is represented by one of the strings 
          'running'
          'no workflow'
          'error'
          'finished'
    '''
    target = get_target(workflow_identifier, source)


    if os.path.exists(os.path.join(target, '/status.running')):
        return 'running'
    if os.path.exists(os.path.join(target, '/status.finished')):
        return 'finished'
    if os.path.exists(os.path.join(target, '/status.error')):
        return 'error'
    return 'no workflow'

    return True

    

def get_workflows(mimetype):
    '''
      Return a list of descriptors of workflows. Each entry is a triple of the 
      form: (identifier, human-readable name, description)
    '''

    ## Select those workflows which have the specified mimetype listed 
    applicable_workflows = [wf for wf in workflows if ('any' in wf['mimetypes'] or mimetype in wf['mimetypes'])]
    
    
    return applicable_workflows