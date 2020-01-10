#!/bin/bash

folder_name=runNN
current_path=`pwd`
echo $current_path
if [ ! -d $folder_name ]; then
   mkdir $current_path/$folder_name
fi
cp `cat files_need.txt` $current_path/$folder_name
cd $current_path/runNN

