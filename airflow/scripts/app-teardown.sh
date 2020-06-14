#!/bin/bash -e
# @script       app-teardown.sh
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @description
# App teardown script.
#
# @usage
# ./app-teardown.sh

echo "***********************"
echo "*** TEARDOWN SCRIPT ***"
echo "***********************"

rm -rf /datalake/transient/jokes/* || true

echo "Execution finished at $(date '+%F %T'). See ya!"
exit 0