#!/usr/bin/env bash

SHARE_DIR=//rivendell/ActiveDevelopmentProjects/ckan
MOUNT_DIR=/mnt/ckan

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if grep -qs "$MOUNT_DIR" /proc/mounts; then
  echo "Backup share already mounted."
else
  # via /etc/fstab
  echo "Mounting..."
  read -p "User: " SMB_USER
  read -sp "Password: " SMB_PASS

  rm -f /root/.smb
  echo "username=$SMB_USER" > /root/.smb
  echo "password=$SMB_PASS" >> /root/.smb

  echo "$SHARE_DIR $MOUNT_DIR cifs credentials=/root/.smb,rw,auto,domain=internal,users 0 0" >> /etc/fstab
  mkdir -p $MOUNT_DIR
  mount -a

  #  # via mount command
  #  mkdir -p $MOUNT_DIR
  #  read -sp 'Enter password: ' PASS
  #  mount -t cifs -o rw,domain=internal,username="$USER",password="$PASS" "$SHARE_DIR" "$MOUNT_DIR"

  if [[ $? -eq 0 ]]; then
   echo "Backup share mounted success!"
  else
   echo "Mounting of backup share failed..."
  fi
fi
