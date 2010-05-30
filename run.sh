#!/bin/bash

python ./sklab/server/run.py $1 &
python ./sklab/run.py $1
