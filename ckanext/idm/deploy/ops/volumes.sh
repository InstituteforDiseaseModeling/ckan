#!/usr/bin/env bash
# TODO: export and backup containers

COMMAND=$1
IN_TAR=$2
TIME_STAMP=$(date +'%Y%m%d-%I%M')
LABEL="$HOSTNAME"_"$TIME_STAMP"
VOLUMES_DIR=/var/lib/docker/volumes/
TMP_DIR=$(mktemp -d)
MIRROR_DIR=/mnt/ActiveDevelopmentProjects/ckan/mirror/$HOSTNAME
BACKUP_DIR=/mnt/ActiveDevelopmentProjects/ckan/backup/$HOSTNAME

function mirror_volumes {
  echo "RSYNC docker volumes."
  mkdir -p /mnt/ActiveDevelopmentProjects/ckan/mirror/$HOSTNAME
  rsync -azvh "$VOLUMES_DIR"/deploy_pg_data/      "$MIRROR_DIR"/deploy_pg_data
  rsync -azvh "$VOLUMES_DIR"/deploy_ckan_storage/ "$MIRROR_DIR"/deploy_ckan_storage
  rsync -azvh "$VOLUMES_DIR"/deploy_solr_data/    "$MIRROR_DIR"/deploy_solr_data

  mkdir -p "$MIRROR_DIR"/deploy_ckan_config
  cp "$VOLUMES_DIR"/deploy_ckan_config/production.ini "$MIRROR_DIR"/deploy_ckan_config/production.ini
}

case  COMMAND  in
      mirror)
            echo "Mirror docker volumes."
            mirror_volumes
            ;;
      backup)
            echo "Archive docker volumes mirror."
            mirror_volumes
            mkdir -p $BACKUP_DIR
            tar -cvzf "$BACKUP_DIR"/docker_volumes_"$LABEL".tar.gz $MIRROR_DIR
            ;;
      restore)
            echo "Restore docker volumes."
            docker-compose down -v

            tar -xzf $2 -C $TMP_DIR
            rsync -r "$TMP_DIR""$MIRROR_DIR"/ $VOLUMES_DIR

            chmod -R 755 $VOLUMES_DIR/deploy_solr_data
            chown -R 8983 $VOLUMES_DIR/deploy_solr_data

            rm -rf $TMP_DIR
            ;;
      *)
esac

