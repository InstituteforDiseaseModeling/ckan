#!/usr/bin/env bash
# TODO: export and backup containers

TIME_STAMP=$(date +'%Y%m%d-%I%M')
LABEL="$HOSTNAME"_"$TIME_STAMP"
VOLUMES_DIR=/var/lib/docker/volumes/
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

  #rsync -azvh /var/lib/docker/volumes/deploy_ckan_config/ /mnt/ActiveDevelopmentProjects/ckan/mirror/$HOSTNAME/deploy_ckan_config
  #rsync -azvh /var/lib/docker/volumes/deploy_ckan_home/ /mnt/ActiveDevelopmentProjects/ckan/mirror/$HOSTNAME/deploy_ckan_home
}

case  $1  in
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
            docker-compose down

            docker volume rm deploy_pg_data
            docker volume rm deploy_ckan_storage
            docker volume rm deploy_solr_data
            docker volume rm deploy_ckan_config
            docker volume rm deploy_ckan_home

            docker volume create deploy_pg_data
            docker volume create deploy_ckan_storage
            docker volume create deploy_solr_data
            docker volume create deploy_ckan_config
            docker volume create deploy_ckan_home

            tmp_dir=/tmp/docker_volumes/"$LABEL"
            mkdir -p $tmp_dir
            tar -xzf $2 -C $tmp_dir
            rsync -r "$tmp_dir""$MIRROR_DIR"/ $VOLUMES_DIR

            chmod -R 755 $VOLUMES_DIR/deploy_solr_data
            chown -R 8983 $VOLUMES_DIR/deploy_solr_data

            rm -rf $tmp_dir
            ;;
      *)
esac

