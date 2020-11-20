# Capacity Prediction
This repo contains a simple pipeline consisting of synthetic network data that is sent to a Kafka topic. The topic is consumed by a service that forecasts the future development of the network data to support network capacity planning. Both, network data and derived forecasts, are stored in elasticsearch.

## Maintainers / Developers
* Niklas Wilcke <niklas.wilcke@uniberg.com>
* Christoph Ölschläger <christoph.oelschlaeger@uniberg.com>
* David Bröhan <david.broehan@uniberg.com>

## Project State
Proof of concept

## Description
TBW

### Pipelines
* Network capacity prediction: csv file --> Flink --> Kafka --> Logstash --> Elasticsearch

### Usage

#### Flink Predictor
To execute the predictor, please ensure to have at least assigned 8 GB of RAM and 4 cores to your docker daemon.
If your hardware does not support this, decrease these values, but also decrease the `parallelism.default` of the jobmanager service and the `taskmanager.memory.process.size` of the taskmanager service in the `docker-compose.yml` file. Try to roughly keep a ratio from 1 to 3000 MB RAM.

```
# Pull all images
docker-compose pull
# startup all the needed services.
docker-compose up -d --build
# Wait for services to startup and work
# Import Kibana Dashboard
docker-compose exec kibana ./scripts/import-objects.sh
# Execute prediction job
docker-compose exec jobmanager ./bin/flink run --python src/predict.py
# Visit Kibana on http://localhost:5601 to checkout the results
```

#### Reset Environment
To remove all docker entities and start over from scratch, execute the following command.
```
docker-compose down --volumes
```
