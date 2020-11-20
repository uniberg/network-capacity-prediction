FROM flink:1.12.0-rc1-scala_2.11

LABEL maintainer="Niklas Wilcke <niklas.wilcke@uniberg.com>"

ARG FLINK_VERSION_SHORT=1.12.0
ARG FLINK_VERSION_LONG=1.12.0-rc1
ARG SCALA_VERSION=2.11
ARG ELASTICSEARCH_VERSION=7

# Install python
# TODO: Minimize dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    zip \
  && rm -rf /var/lib/apt/lists/* \
  && ln -s /usr/bin/python3 /usr/bin/python \
  && ln -s /usr/bin/pip3 /usr/bin/pip

# Install Flink Libraries
# Elasticsearch Connector
RUN wget --no-verbose -P /opt/flink/lib/ "https://repository.apache.org/content/repositories/orgapacheflink-1402/org/apache/flink/flink-sql-connector-elasticsearch${ELASTICSEARCH_VERSION}_${SCALA_VERSION}/${FLINK_VERSION_SHORT}/flink-sql-connector-elasticsearch${ELASTICSEARCH_VERSION}_${SCALA_VERSION}-${FLINK_VERSION_SHORT}.jar"
# Kafka Connector
RUN wget --no-verbose -P /opt/flink/lib/ "https://repository.apache.org/content/repositories/orgapacheflink-1402/org/apache/flink/flink-sql-connector-kafka_${SCALA_VERSION}/${FLINK_VERSION_SHORT}/flink-sql-connector-kafka_${SCALA_VERSION}-${FLINK_VERSION_SHORT}.jar"

# Install pyflink
# Hint: Flink 1.10 seems to need additional dependencies, like defined in script the setup-pyflink-virtual-env.sh
#RUN pip install apache-flink==${FLINK_VERSION}
# Build pyflink from source
RUN wget --no-verbose https://dist.apache.org/repos/dist/dev/flink/flink-1.12.0-rc1/python/apache_flink-1.12.0-cp37-cp37m-manylinux1_x86_64.whl \
  && pip install apache_flink-1.12.0-cp37-cp37m-manylinux1_x86_64.whl \
  && rm apache_flink-1.12.0-cp37-cp37m-manylinux1_x86_64.whl

# Workaround: Install dependencies of fbprophet before building it,
# because they are required for the build process.
COPY --chown=flink ./requirements.txt .
COPY --chown=flink ./constraints.txt .
RUN pip install -r requirements.txt \
  && pip install -c constraints.txt fbprophet==0.7.1

# TODO: Try to get rid of the beam related exceptions in the taskmanager
# I think a dependency is missing
# Did not work
#RUN wget --no-verbose -P /opt/flink/lib/ "https://repo1.maven.org/maven2/org/apache/beam/beam-vendor-grpc-1_21_0/0.1/beam-vendor-grpc-1_21_0-0.1.jar"
# Did not work
#RUN wget --no-verbose -P /opt/flink/lib/ "https://repo1.maven.org/maven2/org/apache/beam/beam-sdks-java-core/2.25.0/beam-sdks-java-core-2.25.0.jar"
# Could go into the right direction. It is still working, but there are other Exceptions now.
# RUN ln -s "/opt/flink/opt/flink-python_${SCALA_VERSION}-${FLINK_VERSION_SHORT}.jar" /opt/flink/lib/
