#!/bin/bash

## This script starts a serial simulation.

current_path=`pwd`

cd $current_path

#cd /home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final

molaris_hpc9.15 2zf0_ac_start.inp > 2zf0_ac_start.out
