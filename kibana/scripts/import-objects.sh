#!/bin/bash

script_path=$(dirname $(readlink -f $0))

curl -X POST "localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form "file=@${script_path}/kibana-objects.ndjson"

