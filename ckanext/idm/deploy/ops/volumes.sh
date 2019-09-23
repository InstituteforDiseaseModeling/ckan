#!/usr/bin/env bash

COMMAND=$1
IN_TAR=$2
CKAN_ENV=${3:-prod}

LABEL=_"$HOSTNAME"_"$(date +'%Y%m%d-%I%M')"
BACKUP_DIR=/mnt/ActiveDevelopmentProjects/ckan/backup/$HOSTNAME

# Ensure working dir
my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $my_dir

function tar_volumes {
  dst_dir=$1
  label=$2
  dst_file=docker_volumes"$label".tar.gz

  mkdir -p $dst_dir
  echo Backing up "$dst_file"
  docker run -it --rm --name=backup --volumes-from=ckan --volumes-from=db --volumes-from=solr -v=$dst_dir/:/backup alpine \
    tar -cvzf /backup/"$dst_file" /var/lib/ckan /var/lib/postgresql/data /opt/solr/server/solr/ckan/data
}

function restore_volumes {
  src_dir=$(dirname "$1")
  tar_file=$(basename "$1")

  read -p "Are you sure?"
  echo

  if [[ $REPLY =~ delete-all-data ]]
  then
    cd ..
    echo Step 1: Removing containers and volumes
    docker rm -f ops
    docker-compose down -v
    docker-compose up -d ckan db solr

    echo Step 2: Starting ops container
    docker run --rm -d --name=ops --volumes-from=ckan --volumes-from=db --volumes-from=solr -v="$src_dir"/:/backup alpine tail -F anything
    docker ps
    docker-compose down

    echo Step 3: Restoring "$tar_file"
    docker exec ops tar -C / -xzf /backup/"$tar_file"
    docker stop ops

    echo Step 4: Running "$CKAN_ENV"-up
    bash deploy.sh "$CKAN_ENV"-up

  else
    echo Incorrect confirmation phrase...exiting.
    exit 1
  fi
}

case  $COMMAND  in
      mirror)
            echo "Mirror docker volumes."
            tar_volumes "$BACKUP_DIR" 'MIRROR'
            ;;
      backup)
            echo "Backup docker volumes."
            tar_volumes "$BACKUP_DIR" "$LABEL"
            ;;
      restore)
            echo "Restore docker volumes."
            restore_volumes "$IN_TAR"
            ;;
      *)
esac

