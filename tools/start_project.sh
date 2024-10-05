#!/bin/bash
# A Script to jump start a project.
DEMO_NAME=owl-demo-base

if [[ $# -eq 1 ]]; then
    DEMO_NAME=$1
fi

if [ ! -d $DEMO_NAME ]; then
    mkdir $DEMO_NAME
fi

cd $DEMO_NAME
if [ ! -f .env ]; then
    curl -X GET https://https://raw.githubusercontent.com/AthenaDecisionSystems/athena-owl-core/refs/heads/main/tools/.env_tmpl .env
fi
curl -X GET https://github.com/AthenaDecisionSystems/athena-owl-core/tree/main/tools/demo_tmpl.zip 