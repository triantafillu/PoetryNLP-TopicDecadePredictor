#!/bin/bash
# Builds a docker image for myproject
# takes 1 argument which is the name of a dockerfile e.g. train-gpu.Dockerfile

echo "enter a dockerfile as an argument e.g. 'source utils/builddocker.sh train-cpu.Dockerfile'"
echo ""
echo "options are:"
ls install/ | grep 'Dockerfile'
echo "building docker image for $1"

sudo docker build -t poems_analyzer install/ -f install/$1

echo "Done!"