# IDM CKAN: Deploy and Run

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

      conda create -n ckan python=2.7

- Using Python 2.7 virtualenv

      pip install virtualenv
      virtualenv -p C:\Python27\python.exe  D:\Virtual_ckan; 
      D:\Virtual_ckan\Scripts\activate

#### Apply Windows specific change in source
To run on Windows locally, few minor source changes are needed. 

Use file comparison tool to see which lines have to be modified:

    C:\git\ckan\ckanext\idm\deploy\windows-local\source_change\before
    C:\git\ckan\ckanext\idm\deploy\windows-local\source_change\after

#### Run local setup

Set up locally and run it from the command line (to confirm the setup was successful).

    cd c:\git\ckan\ckanext\idm\deploy\windows-local     
    setup.cmd
    docker stop ckan
    START paster serve development.ini
    explorer http://localhost:5000/   

#### Debug with PyCharm
 
Debug with PyCharm using paster.py and the below configuration  

    In PyCharm open Run, Edit Configuration as set:  
    
    Script path: 
    C:\git\ckan\ckanext\idm\deploy\windows-local\paster.py   
    
    Parameters: 
    serve development.ini  

#### Verify by running from docker-compose 
Build Docker image using the latest CKAN code and run all components as Docker containers.  

    cd c:\git\ckan\ckanext\idm\deploy 
    run-docker-compose.cmd stage  
    explorer http://localhost:5000/  
  

    
## Deploy to Production  

Windows:

    cd c:\git\ckan\ckanext\idm\deploy 
    run-docker-compose.cmd prod  
    explorer http://localhost:5000/  

CentOS 7

    cd c:\git\ckan\ckanext\idm\deploy
    chmod +x deploy.sh 
    ./deploy.sh
        
    # On the host machine open ports:
    firewall-cmd --permanent --add-port=5000/tcp
    firewall-cmd --permanent --add-port=8800/tcp
    firewall-cmd --reload


... more coming soon...

###### References  
How to install on Windows 7:  
https://github.com/ckan/ckan/wiki/How-to-Install-CKAN-2.5.2-on-Windows-7  
Installing from docker-compose:  
https://docs.ckan.org/en/latest/maintaining/installing/install-from-docker-compose.html

