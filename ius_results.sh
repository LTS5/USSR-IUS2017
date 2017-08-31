#!/bin/bash

# Create a results folder in case it does not exist
if [ ! -d "results" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir results
  cd "results"
  mkdir "das"
  mkdir "FISTA"
  mkdir "FISTALP"
  cd ..
fi

echo "*****************************   Downloading the data   *****************************"
python setup_ius.py

echo "*****************************   Launching the image reconstruction scripts   *****************************"
python launch_ius_scripts.py $1


echo "*****************************   Launching the scripts generating the metrics   *****************************"
cd matlab
matlab -nodesktop -nojvm -r "generate_metrics({'../results/das', '../results/FISTA', '../results/FISTALP'}); exit;"

echo "*****************************   Launching the scripts generating the figures   *****************************"
matlab -nodesktop -r "generate_figures({'../results/das', '../results/FISTA', '../results/FISTALP'});exit;"
