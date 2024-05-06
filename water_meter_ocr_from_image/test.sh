#!/bin/bash

docker run \
  --rm \
  -it \
  --name builder \
  --privileged \
  -v $PWD:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/home-assistant/amd64-builder \
  -t /data \
  --all \
  --test \
  -i my-test-addon-{arch} \
  -d local

docker run \
  --rm \
  -v ./test_data:/data \
  local/my-test-addon-amd64