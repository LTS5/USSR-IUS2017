#!/bin/bash

# Create a results folder in case it does not exist
if [ ! -d "results" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir -p results/das
  mkdir -p results/FISTA
  mkdir -p results/FISTALP
fi

echo "*****************************   Downloading the data   *****************************"
python setup_ius.py

echo "*****************************   Launching the image reconstruction scripts   *****************************"
python launch_ius_scripts.py $1

echo "*****************************   Launching the scripts generating the metrics   *****************************"
cd matlab
CURR_PATH=$(pwd)
matlab -nodesktop -nojvm -nosplash -r "cd '$CURR_PATH'; generate_metrics({'../results/das', '../results/FISTA', '../results/FISTALP'}); exit;"

echo "*****************************   Launching the scripts generating the figures   *****************************"
matlab -nodesktop -nosplash -r "cd '$CURR_PATH'; generate_figures({'../results/das', '../results/FISTA', '../results/FISTALP'}); exit;"
