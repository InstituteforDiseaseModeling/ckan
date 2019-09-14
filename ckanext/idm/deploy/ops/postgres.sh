#!/usr/bin/env bash

TIME_STAMP=$(date +'%Y%m%d-%I%M')
LABEL="$HOSTNAME"_"$TIME_STAMP"
BACKUP_DIR=/mnt/ActiveDevelopmentProjects/ckan/backup/$HOSTNAME

case  $1  in
      backup)
            #https://docs.ckan.org/en/2.8/maintaining/database-management.html
            #docker exec db pg_dump --format=custom -d ckan_default > ckan.dump

            docker exec db pg_dumpall -c --if-exists -U ckan -w > /tmp/postgres_"$LABEL".sql
            tar -cvzf "$BACKUP_DIR"/postgres_"$LABEL".tar.gz -C /tmp postgres_"$LABEL".sql
            rm /tmp/postgres_"$LABEL".sql
            ;;
      restore)
            #https://docs.ckan.org/en/2.8/maintaining/database-management.html
            #docker exec ckan paster db clean -c /etc/ckan/default/production.ini
            #docker exec db pg_restore --clean --if-exists -d ckan_default < ckan.dump

            file_name="$(basename -- $2)"
            tar -xzf $2 > /tmp/"$file_name"
            docker cp /tmp/"$file_name" db:/tmp/"$file_name"
            docker exec db psql -U ckan -w -f /tmp/"$file_name"
            docker exec db rm /tmp/"$file_name"
            rm /tmp/"$file_name"
            ;;
      *)
esac

