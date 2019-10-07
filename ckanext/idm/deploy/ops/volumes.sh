#!/usr/bin/env bash

COMMAND=$1
INTERVAL=${2:-test}
RESTOR_TAR=$2
CKAN_ENV=${3:-prod}

LABEL=_"$HOSTNAME"_"$(date +'%Y%m%d-%I%M')"
SHARES_DIR=/mnt/ckan
BACKUP_DIR="$SHARES_DIR"/backup/"$HOSTNAME"/"$INTERVAL"

function tar_volumes {
  dst_dir=$1
  label=$2
  dst_file=docker_volumes"$label".tar.gz

  mkdir -p $dst_dir
  echo Backing up "$dst_file"
  docker run --rm --name=backup --volumes-from=ckan --volumes-from=db --volumes-from=solr -v=$dst_dir/:/backup alpine \
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
    # Ensure working dir
    ops_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    bash deploy.sh "$CKAN_ENV"-up

  else
    echo Incorrect confirmation phrase...exiting.
    exit 1
  fi
}

function remove_old_backups {
  dst_dir=${1}
  days=${2}
  find "$dst_dir"/ -name "*.tar.gz" -type f -mtime +"$days" -exec rm -f {} \;
}

case  $INTERVAL in
      hourly)
            RETAIN_DAYS=1;;
      daily)
            RETAIN_DAYS=60;;
      weekly)
            RETAIN_DAYS=365;;
      test)
            RETAIN_DAYS=1;;
      *)
            RETAIN_DAYS=10000;;
esac

case  $COMMAND  in
      backup)
            echo "Backup docker volumes."
            remove_old_backups "$BACKUP_DIR" "$RETAIN_DAYS"
            tar_volumes "$BACKUP_DIR" "$LABEL"
            ;;
      restore)
            echo "Restore docker volumes."
            restore_volumes "$RESTOR_TAR"
            ;;
      *)
esac

