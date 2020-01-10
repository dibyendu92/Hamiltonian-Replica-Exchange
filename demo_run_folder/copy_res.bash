#!/bin/bash

##This script copies the restart files from different acrun_0XX folder generated after parallel productive runs. 

current_path=`pwd`
cd $current_path
#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

for i in {1..21}
do 
   cp $current_path/output/acrun_`printf "%03d" $i`/ac.res`printf "%03d" $i` $current_path
done

#cp /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final/output/pdb_gen/*.pdb /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final



