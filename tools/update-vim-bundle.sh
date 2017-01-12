#!/bin/bash

set -e

cd ~/.vim/bundle

for d in *
do
    cd $d
    echo "Updating $d..."
    git pull
    cd ..
done
