#!/bin/sh
set -e

python app/utils/init_opensearch.py
python app/utils/load_data.py
$@ $CMD