#!/bin/bash

THIS_PATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
echo `dirname $THIS_PATH` added to PYTHONPATH

export PYTHONPATH=$PYTHONPATH:`dirname ${THIS_PATH}`
