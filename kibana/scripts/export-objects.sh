#!/bin/bash

script_path=$(dirname $(readlink -f $0))

curl -X POST "localhost:5601/api/saved_objects/_export" -o "${script_path}/kibana-objects.ndjson" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d '
{
  "type": ["index-pattern", "dashboard", "visualization"],
  "excludeExportDetails": true 
}
'
