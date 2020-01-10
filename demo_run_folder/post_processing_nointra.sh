#!/usr/bin/bash

current=`pwd`

for f in `ls -d */`
do 
  cd $f
  for j in `ls -d */`
     do 
       cp  ../map_ac.inp $current/$f$j  #proc_nointra.py'
#       cp  ../map_extract_nointra.py $current/$f$j'map_folder/' #map_extract_noitra.py'
       cd $current/$f$j
#       rm output.txt
#       python map_extract_nointra.py
#       python proc_nointra.py
	mapping_hpc9.15 <map_ac.inp > map_ac.out
        echo $f$j
	grep -a "Average mapping" map_ac.out
       cd $current/$f
#     cd $f$j'map_folder'
#     cd ../../
     done
  cd $current
  done 
