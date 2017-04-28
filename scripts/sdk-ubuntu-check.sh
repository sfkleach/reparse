#!/bin/bash
apt-get update && apt-get upgrade -y && apt-get install -y make git
mkdir -p projects/reparse
cd projects/reparse
git -C /tmp/reparse archive master | tar xf -
make sdk-ubuntu
make clean && make build && make check
