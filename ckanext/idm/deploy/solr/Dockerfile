FROM solr:6.6.5
MAINTAINER Open Knowledge

# Enviroment
ENV SOLR_CORE ckan

# Create Directories
RUN mkdir -p /opt/solr/server/solr/$SOLR_CORE/conf
RUN mkdir -p /opt/solr/server/solr/$SOLR_CORE/data

# Adding Files
ADD ./ckanext/idm/deploy/solr/solrconfig.xml \
./ckanext/idm/deploy/solr/schema.xml \
./ckanext/idm/deploy/solr/currency.xml \
./ckanext/idm/deploy/solr/synonyms.txt \
./ckanext/idm/deploy/solr/stopwords.txt \
./ckanext/idm/deploy/solr/protwords.txt \
./ckanext/idm/deploy/solr/elevate.xml \
/opt/solr/server/solr/$SOLR_CORE/conf/

# Create Core.properties
RUN echo name=$SOLR_CORE > /opt/solr/server/solr/$SOLR_CORE/core.properties

# Giving ownership to Solr

USER root
RUN chown -R $SOLR_USER:$SOLR_USER /opt/solr/server/solr/$SOLR_CORE

# User
USER $SOLR_USER:$SOLR_USER
