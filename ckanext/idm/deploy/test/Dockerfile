FROM docker_ckan

USER root

RUN apt-get update -yq \
    && apt-get install curl gnupg -yq \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs -yq \
    && apt-get update -yq \
    && apt-get install libfontconfig -yq \
    && apt-get update -yq \
    && apt-get install git-core vim -yq \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r $CKAN_HOME/dev-requirements.txt

COPY test-requirements.txt .
RUN pip install --no-cache-dir -r test-requirements.txt

WORKDIR $CKAN_HOME

RUN npm install mocha-phantomjs@3.5.0 && \
    npm install phantomjs@~1.9.1

COPY *.sh *.ini $CKAN_HOME/ckanext/idm/deploy/test/

RUN chown -R ckan $CKAN_HOME/ckanext/idm/deploy/test && \
    chmod +x $CKAN_HOME/ckanext/idm/deploy/test/run-tests.sh

USER ckan

CMD $CKAN_HOME/ckanext/idm/deploy/test/run-tests.sh
