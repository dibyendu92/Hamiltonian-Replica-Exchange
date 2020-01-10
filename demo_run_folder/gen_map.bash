#!/bin/bash

## This scipt makes a folder called 'map_folder' if it is not already present at the working directory and then copy all map_ac.gap0XX files
## to this 'map_folder'. The map files are copied from acrun_0XX folders inside ./output/ 

current_path=`pwd`
cd $current_path

if [ ! -d "map_folder" ]; then
   mkdir map_folder
fi

for f in $(seq -f "%03g" 1 21)
do
     cp $current_path/output/acrun_$f/map_ac.gap$f $current_path/map_folder
done




