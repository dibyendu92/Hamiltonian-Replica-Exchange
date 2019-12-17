#!/bin/bash

#A Demo bash script to prepare script for checking runs parallelly
#Dont bother program would make this file for you

current_folder=`pwd`

cd $current_folder

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 ac_001.inp > ac_001.out 2>&1 &
molaris_hpc9.15 ac_002.inp > ac_002.out 2>&1 &
molaris_hpc9.15 ac_003.inp > ac_003.out 2>&1 &
molaris_hpc9.15 ac_004.inp > ac_004.out 2>&1 &
molaris_hpc9.15 ac_005.inp > ac_005.out 2>&1 &
molaris_hpc9.15 acswap_001.inp > acswap_001.out 2>&1 &
molaris_hpc9.15 acswap_002.inp > acswap_002.out 2>&1 &
molaris_hpc9.15 acswap_003.inp > acswap_003.out 2>&1 &
molaris_hpc9.15 acswap_004.inp > acswap_004.out 2>&1 &
molaris_hpc9.15 acswap_005.inp > acswap_005.out 2>&1 &
