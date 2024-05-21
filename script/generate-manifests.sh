#!/usr/bin/env bash

set -e

GENDIR=".generated/"

while getopts "d:" opt; do
    case $opt in
        d)
            GENDIR=${OPTARG}
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
        ;;
    esac
done

mkdir -p "$GENDIR"

for d in $(find ./apps ./tools -name "overlays" -type d); do
  for overlay in "$d"/*; do
    echo "Generating manifests $GENDIR/$overlay/manifests.yaml"
    mkdir -p "$GENDIR/$overlay"
    kubectl kustomize "$overlay" > "$GENDIR/$overlay/manifests.yaml" || continue
  done
done
