#!/usr/bin/env bash

# only check secrets by default (same as CI/CD)
if ! trivy fs . ; then
    echo "Security check failed"
    exit 1
fi

# extra checks
trivy fs  --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL --scanners misconfig --misconfig-scanners kubernetes  --quiet --no-progress --ignore-unfixed .qq

checkov --directory apps --directory tools --quiet --framework dockerfile,kustomize --skip-results-upload
