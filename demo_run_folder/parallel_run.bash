#!/bin/bash

##This file makes bash scirpt to run parallel jobs from the current working directory

current_path=`pwd`

cd $current_path

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 acrun_001.inp > acrun_001.out 2>&1 &
molaris_hpc9.15 acrun_002.inp > acrun_002.out 2>&1 &
molaris_hpc9.15 acrun_003.inp > acrun_003.out 2>&1 &
molaris_hpc9.15 acrun_004.inp > acrun_004.out 2>&1 &
molaris_hpc9.15 acrun_005.inp > acrun_005.out 2>&1 &
molaris_hpc9.15 acrun_006.inp > acrun_006.out 2>&1 &
molaris_hpc9.15 acrun_007.inp > acrun_007.out 2>&1 &
molaris_hpc9.15 acrun_008.inp > acrun_008.out 2>&1 &
molaris_hpc9.15 acrun_009.inp > acrun_009.out 2>&1 &
molaris_hpc9.15 acrun_010.inp > acrun_010.out 2>&1 &
molaris_hpc9.15 acrun_011.inp > acrun_011.out 2>&1 &
molaris_hpc9.15 acrun_012.inp > acrun_012.out 2>&1 &
molaris_hpc9.15 acrun_013.inp > acrun_013.out 2>&1 &
molaris_hpc9.15 acrun_014.inp > acrun_014.out 2>&1 &
molaris_hpc9.15 acrun_015.inp > acrun_015.out 2>&1 &
molaris_hpc9.15 acrun_016.inp > acrun_016.out 2>&1 &
molaris_hpc9.15 acrun_017.inp > acrun_017.out 2>&1 &
molaris_hpc9.15 acrun_018.inp > acrun_018.out 2>&1 &
molaris_hpc9.15 acrun_019.inp > acrun_019.out 2>&1 &
molaris_hpc9.15 acrun_020.inp > acrun_020.out 2>&1 &
molaris_hpc9.15 acrun_021.inp > acrun_021.out 2>&1 &
