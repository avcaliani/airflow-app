#!/bin/bash -e
# @script       app-init.sh
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @description
# App initialization script.
#
# @usage
# ./app-init.sh

echo "*****************************"
echo "*** INITIALIZATION SCRIPT ***"
echo "*****************************"

echo "Creating data lake directories..."
mkdir -p /datalake/ && cd /datalake
mkdir -p logs/app-broken \
    logs/app-extractor \
    logs/app-processor

echo "Done. See ya!"
exit 0