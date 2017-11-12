import pip

def install(package):
    pip.main(['install', package])

### Install Packages for AWS
install('awscli')   ### AWS CLI: Amazon Web Services Command Line Interface
install('boto3')    ### Boto3: Python3 SDK for AWS