#!/bin/bash

#Demo bash script to prepare script for parallel check runs

current_folder=`pwd`

cd $current_folder

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 ac_0XX.inp > ac_0XX.out 2>&1 &
molaris_hpc9.15 acswap_0XX.inp > acswap_0XX.out 2>&1 &
