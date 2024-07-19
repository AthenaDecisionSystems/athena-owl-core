#!/bin/bash
DEMO_NAME=owl-demo-base

if [[ $# -eq 1 ]]; then
    DEMO_NAME=$1
fi

if [ ! -d $DEMO_NAME ]; then
    mkdir $DEMO_NAME
fi

cd $DEMO_NAME
if [ ! -f .env ]; then
    cp ../tools/.env_tmpl .env
fi
cp -r ../tools/demo_tmpl/* .