#!/bin/sh

echo "Stopping cluster.."
docker stop $(docker ps -q --filter ancestor=gaiaadm/pumba )
docker compose stop
