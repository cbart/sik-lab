#!/bin/bash

THIS_PATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
echo $THIS_PATH added to PYTHONPATH

export PYTHONPATH=$PYTHONPATH:${THIS_PATH}
