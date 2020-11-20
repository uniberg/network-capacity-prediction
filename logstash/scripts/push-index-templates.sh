#!/bin/bash

index_template_dir="/usr/share/logstash/index-templates/"

es_host=${ES_HOST_1:-elasticsearch}

for filepath in "${index_template_dir}"*.json; do
  filename=${filepath##*/}
  template_name=${filename%.json}
  echo "Updating index template ${template_name}"
  curl -XPUT "http://${es_host}:9200/_template/${template_name}" -H "Content-Type: application/json" -d "@${filepath}"
  echo ""
done
