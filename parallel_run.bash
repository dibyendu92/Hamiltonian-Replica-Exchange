#!/bin/bash

##This is a bash scirpt to run parallel jobs from the current working directory
##Dont bother, the program would make one for you

current_path=`pwd`

cd $current_path

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 acrun_001.inp > acrun_001.out 2>&1 &
molaris_hpc9.15 acrun_002.inp > acrun_002.out 2>&1 &
molaris_hpc9.15 acrun_003.inp > acrun_003.out 2>&1 &
molaris_hpc9.15 acrun_004.inp > acrun_004.out 2>&1 &
molaris_hpc9.15 acrun_005.inp > acrun_005.out 2>&1 &
