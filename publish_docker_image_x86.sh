#!/bin/bash
. build_209_web_docker.sh
docker login
docker tag w209_proj_don_irwin donirwinberkeley/w209_proj_don_irwin:x86_latest
docker push donirwinberkeley/w209_proj_don_irwin:x86_latest
