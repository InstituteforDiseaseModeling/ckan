# Setup production (stage) docker host environment  

### Requirements
- CentOS 7.5 or 7.6
- Docker 19.03.2
- docker-compose 1.23.2
- git version 1.8.3.1
- cifs-utils 6.2-10.el7 


### Install docker   
Run below instructions.
  
    # Install docker 19.03.2
    sudo yum install -y yum-utils device-mapper-persistent-data lvm2  
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo  
    sudo yum install -y docker-ce-19.03.2-3.el7               
    
    # Start docker
    sudo systemctl start docker  
    sudo docker --version
    
    # Enable docker without sudo 
    sudo usermod -aG docker $USER  
    
    # Log out, then in again and run to confirm:  
    docker run hello-world  
    
For more information see: https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/centos/

### Install docker-compose  

    # Install docker-compose 1.23.2  
    sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose  
    sudo chmod +x /usr/local/bin/docker-compose  
    
    # To allow sudo to see docker-compose  
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose  
    docker-compose --version  


### Install git 
    # Install git version 1.8.3.1
    sudo yum install git  


### Install CIFS mount utilities
This is required for mounting the backup share.
  
    sudo yum install -y cifs-utils
    
The deploy script will mount the backup share is needed. In case that didn't work, look up instructions online, for example:
https://www.looklinux.com/how-to-mount-samba-share-on-centosfedoraredhat/
https://wiki.centos.org/TipsAndTricks/WindowsShares
