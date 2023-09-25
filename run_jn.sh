#!/bin/bash
if ! [ -n "myproj" ]; then
    if [ -d "./myproj" ]; then
        source ./myproj/bin/activate
    else
        . setup_venv.sh        
    fi
fi

jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="" --NotebookApp.password="" --port=8888 
