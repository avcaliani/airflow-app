#!/bin/sh
# @script       build-images.sh
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @description
# Script to build docker images.
#
# @usage
# ./build-images.sh

docker_build() {
    echo "Building job '$1'..."
    job_path="jobs/$1"
    if test -d "$job_path"; then
        cd "$job_path" && docker build -f "Dockerfile" -t "$1" . && cd -
    else
        echo "ERROR! Job not found '$1'!"
    fi
}

docker_build "app-broken"
docker_build "app-extractor"
docker_build "app-processor"

exit 0