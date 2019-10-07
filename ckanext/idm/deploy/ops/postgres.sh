#!/usr/bin/env bash

COMMAND=$1
INTERVAL=${2:-test}
RESTOR_TAR=$2

LABEL=_"$HOSTNAME"_"$(date +'%Y%m%d-%I%M')"
SHARES_DIR=/mnt/ckan
BACKUP_DIR="$SHARES_DIR"/backup/"$HOSTNAME"/"$INTERVAL"

function tar_pg {
  dst_dir=$1
  label=$2

  mkdir -p $dst_dir
  tar_path="$dst_dir"/postgres"$label".tar.gz
  temp_dir=$(mktemp -d)
  sql_file=postgres"$label".sql

  echo Step 1: Dump all databases into "$tar_path"
  docker exec db pg_dumpall -c --if-exists -U ckan -w > "$temp_dir"/"$sql_file"

  echo Step 2: Tar database dumps
  tar -cvzf "$tar_path" -C "$temp_dir" "$sql_file"
  rm -fR "$temp_dir"
}

function restore_pg {
  tar_path="$1"

  read -p "Are you sure?"
  echo

  if [[ $REPLY =~ delete-all-data ]]
  then
    sql_file=postgres.sql
    temp_dir=$(mktemp -d)
    sql_path="$temp_dir"/"$sql_file"

    echo Step 1: Extract backup tar into "$sql_path"
    tar -xOzf "$tar_path" > "$sql_path"

    echo Step 2: Apply sql dump to db container
    docker cp /"$sql_path" db:/tmp/"$sql_file"
    docker exec db psql -U ckan -w -f /tmp/"$sql_file"
    docker exec db rm /tmp/"$sql_file"
    rm "$sql_path"

    sleep 10
    echo Step 3: Reindex Solr
    docker exec ckan paster search-index rebuild -c /etc/ckan/production.ini
  else
    echo Incorrect confirmation phrase...exiting.
    exit 1
  fi
}

case $COMMAND  in
      backup)
            echo "Backup postgres dumps"
            tar_pg "$BACKUP_DIR" "$LABEL"
            ;;
      restore)
            echo "Restore postgres dump tar"
            restore_pg "$RESTOR_TAR"
            ;;
      *)
esac

