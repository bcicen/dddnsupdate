#!/bin/bash

[ -z "$BIND_HOST" ] && {
  echo "Env variable BIND_HOST must be set"
  exit 1 
}

[ -z "$DOCKER_HOSTS" ] && {
  echo "Env variable DOCKER_HOSTS must be set"
  exit 1 
}

[ -z "$UPDATE_INTERVAL" ] && {
  UPDATE_INTERVAL=60
}

[ ! -f /config ] && {
  echo "/config not found, exiting"
  exit 1
}

while :; do
    for DOCKER_HOST in $DOCKER_HOSTS; do
        dddnsupdate --config /config --bindhost $BIND_HOST --dockerurl $DOCKER_HOST 
    done
    sleep $UPDATE_INTERVAL
done
