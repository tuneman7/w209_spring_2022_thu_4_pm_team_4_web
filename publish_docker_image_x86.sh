#!/bin/bash
find . -type d -name __pycache__ -exec rm -r {} \+
rm -rf ./myproj
. build_209_web_docker.sh
docker login
docker tag w209_proj_don_irwin donirwinberkeley/w209_proj_don_irwin:x86_latest
docker push donirwinberkeley/w209_proj_don_irwin:x86_latest
