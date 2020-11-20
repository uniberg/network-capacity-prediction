# Logstash
This project provides a base image for logstash. It adds some "features" to the standard logstash, which can be found in the following folders.
* `index-templates` contains index templates for all our data sources
* `pipeline` contains all the pipeline definitions
* `scripts` contains some tools
  * `push-index-templates.sh` pushes all the index templates located in `index-templates` to elasticsearch.
