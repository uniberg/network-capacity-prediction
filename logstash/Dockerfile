FROM docker.elastic.co/logstash/logstash:7.10.0

# We don't need this example file
RUN rm /usr/share/logstash/pipeline/logstash.conf

COPY --chown=logstash:root scripts /usr/share/logstash/scripts

# Make our scripts executable
RUN chmod +x /usr/share/logstash/scripts/*

# GID is set to 0 (root) to keep it aligned with the Logstash base image.
# They did this for compatibility reasons with Openshift.
COPY --chown=logstash:root config/pipelines.yml /usr/share/logstash/config/pipelines.yml
COPY --chown=logstash:root index-templates /usr/share/logstash/index-templates
COPY --chown=logstash:root pipeline /usr/share/logstash/pipeline
COPY --chown=logstash:root scripts /usr/share/logstash/scripts
