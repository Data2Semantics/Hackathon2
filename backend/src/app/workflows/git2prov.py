from app import app

def run(workflow, source, target):
    app.logger.debug("{}, {}, {}".format(workflow, source, target))
    
    return True
