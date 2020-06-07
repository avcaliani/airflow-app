#!/bin/sh -e
# @script       run.sh
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @description
# Dummy Bash Job. The "LOG_PATH" environment variable is required.
#
# @usage
# ./run.sh

JOB_NAME="app-broken"
JOB_VERSION="1.0.0"
LOG_FILE="$LOG_PATH/$JOB_NAME.$JOB_VERSION.$(date '+%Y%m%d%H%M%S').log"

info() {
    echo "[$(date '+%F %T')] $1" >> "$LOG_FILE"
    echo "$1"
}

info "Job: $JOB_NAME"
info "Job Version: $JOB_VERSION"
info "Project: airflow"

info "Trying to process... "
sleep 15
status=$(( RANDOM % 2 ))
info "Job finished with status '$status'. Log file created at: $LOG_FILE."

exit $status
