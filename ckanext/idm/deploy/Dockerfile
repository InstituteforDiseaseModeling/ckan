FROM debian:stretch

# Install required system packages
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive \
    && apt-get -q -y install \
        python-dev \
        python-pip \
        python-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libgeos-dev \
        libssl-dev \
        libffi-dev \
        postgresql-client \
        build-essential \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*


# Define environment variables
ENV CKAN_HOME /home/ckan/src/ckan
ENV CKAN_CONFIG /etc/ckan
ENV CKAN_STORAGE_PATH=/var/lib/ckan

# Build-time variables specified by docker-compose.yml / .env
ARG CKAN_SITE_URL

RUN useradd -r -u 900 -m -c "ckan account" ckan
# -s /bin/false ckan
# -d $CKAN_HOME -s /bin/false ckan

COPY requirement*.txt $CKAN_HOME/
RUN pip install --no-cache-dir -r $CKAN_HOME/requirement-setuptools.txt && \
    pip install --no-cache-dir -r $CKAN_HOME/requirements.txt && \
    pip install --no-cache-dir -r $CKAN_HOME/requirements-scheming.txt

RUN mkdir -p $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    ln -s /usr/local/bin/paster /usr/local/bin/ckan-paster

ADD . $CKAN_HOME/

# Install CKAN
RUN pip install -e $CKAN_HOME/ && \
    ln -s $CKAN_HOME/ckan/config/who.ini $CKAN_CONFIG/who.ini && \
    cp -v $CKAN_HOME/ckanext/idm/deploy/ckan-entrypoint.sh /ckan-entrypoint.sh && \
    chmod +x /ckan-entrypoint.sh && \
    chown -R ckan:ckan $CKAN_HOME $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    chmod a-x $(find $CKAN_HOME -name "*.py" -type f)

USER ckan

#ENTRYPOINT ["/ckan-entrypoint.sh"]
WORKDIR $CKAN_HOME
EXPOSE $CKAN_PORT

MAINTAINER Institute for Disease Modeling

#CMD ["paster","serve","/etc/ckan/production.ini"]
