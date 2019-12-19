#!/bin/bash

##This is a demo file to make a bash scirpt to run parallel jobs from the current working directory

current_path=`pwd`

cd $current_path

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 acrun_0XX.inp > acrun_0XX.out 2>&1 &
