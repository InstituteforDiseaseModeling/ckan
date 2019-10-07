# IDM CKAN: Deploy and Run
    
## Deploy to Production  

Setup CentOS 7 docker host machine per instructions in the [ops/README.md](ops/README.md).  
 
Clone the GitHub repo  
 
    mkdir -p /home/ckan
    clone -b 0-idm-proto https://github.com/InstituteforDiseaseModeling/ckan/tree/0-idm-proto /home/ckan/ckan

Run the deploy script (1st time):        

    cd /home/ckan/ckan/ckanext/idm/deploy         
    sudo chmod +x deploy.sh 
    sudo ./deploy.sh boot-prod
    

Refresh the "build" with the latest changes from GitHub:
  
    sudo ./deploy.sh refresh-prod


In case the port is not open add it:  

    # On the host machine open ports:
    firewall-cmd --permanent --add-port=5000/tcp
    firewall-cmd --reload

Note: To setup Stage environment use above instructions and replace 'prod' with 'stage'.

## Automated Tests 

#### Run tests

###### Windows 

    cd c:\git\ckan\ckanext\idm\deploy\test 
    run-docker-compose.cmd run  
    
The results are stored in 
 
    C:\Users\dlukacevic\ckan\test_results

###### Linux:
    cd ~/ckan/ckanext/idm/deploy/test 
    ./run-docker.sh   
      
The results are stored in 
 
    ~/ckan/test_results

#### Customize test run
 
To customize test run set one or more of the "CKAN_TEST_..." environment variables listed in the "test/.env" file.

For example, this will change the test results dir and run only a subset of tests

    export CKAN_TEST_RESULTS_OUT=/test_results 
    export CKAN_TEST_1=./ckan/tests/model/test_tags.py
    export CKAN_TEST_2=./ckanext/idm
    
For troubleshooting, you can disable test execution and keep ckan-test container running by setting:

    export CKAN_TEST_RUN=False

## Windows Development Environment 

#### Create Python virtual environment 

Create Python 2.7 virtual environment using Anaconda or using virtualenv 

- Using Anaconda (latest):

      conda create -n ckan python=2.7 -y
      activate ckan

- Using Python 2.7 virtualenv

      pip install virtualenv
      virtualenv -p C:\Python27\python.exe  D:\Virtual_ckan; 
      D:\Virtual_ckan\Scripts\activate

#### Run local setup

Run as administrator:

    cd c:\git\ckan\ckanext\idm\deploy\windows-local         
    setup.cmd

After setup is complete, the script will open the CKAN home page. Try using it to confirm the setup was successful.

#### Debug with PyCharm
 
Debug with PyCharm using paster.py and the below configuration  

    In PyCharm open Run, Edit Configuration as set:  
    
    Script path: 
    C:\git\ckan\ckanext\idm\deploy\windows-local\paster.py   
    
    Parameters: 
    serve development.ini  
    
    Working directory:  
    C:\git\ckan\ckanext\idm\deploy\windows-local  
    
#### Verify by running from docker-compose
 
Build Docker image using the latest CKAN code and run all components as Docker containers.  

    cd c:\git\ckan\ckanext\idm\deploy 
    run-docker-compose.cmd stage  
    explorer http://localhost:5000/  
    

###### References  
How to install on Windows 7:  
https://github.com/ckan/ckan/wiki/How-to-Install-CKAN-2.5.2-on-Windows-7  
Installing from docker-compose:  
https://docs.ckan.org/en/latest/maintaining/installing/install-from-docker-compose.html  

Scheming
https://github.com/ckan/ckanext-scheming
Temporal search (modified and merged into IDM extension)
https://github.com/EUDAT-B2FIND/ckanext-datesearch


