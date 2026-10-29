#!/bin/bash
# Builds all three DIFFERENT images (v1, v2, v3) from one folder, whatever branch is checked out.
set -e
for n in 1 2 3; do
  docker build --build-arg VERSION=$n -t bhavatharene12/multimoduleapp:v$n .
done
docker images bhavatharene12/multimoduleapp
