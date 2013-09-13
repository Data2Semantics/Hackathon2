import os,sys

def convertToODS(filepath):

    f = open(filepath)
    
    xls = NamedTemporaryFile(delete=False)
    xls.write(f.read())
    xls.close()
    
    xls_filename = xls.name
    ods_filename = xls.name + ".ods"
    
    print "TempFile: ", xls_filename

    
    python_path = app.config['LIBRE_OFFICE_PYTHON_PATH']
    unoconv_path = app.config['UNOCONV_PATH']
    
    print "Calling ", ' '.join([python_path, unoconv_path, '-f', 'ods', xls_filename])
    subprocess.call([python_path, unoconv_path, '-f', 'ods', xls_filename])
    
    return ods_filename


filepath=""
