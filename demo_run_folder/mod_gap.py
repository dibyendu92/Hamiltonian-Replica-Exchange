#!/usr/bin/env python

## This script changes the first line of the map_ac.gap0XX files. The gap files that have been generated during a parallel ac run, have wrong density 
## contribution at the first line of the files. By running this script the file would be automatically changed with right densities(lambda). 

import shutil
num_tasks=21
gap_files=[]
new_files=[]
mod_list=[]
for i in range(1,num_tasks+1):
    gap_files.append("map_ac.gap"+"%03d"%i)
    shutil.copy(gap_files[i-1],"new_"+"map_ac.gap"+"%03d"%i)
for j in range(1,num_tasks+1):
    fo=open("new_" + "map_ac.gap"+"%03d"%j,'r')
    fw=open(gap_files[j-1],'w')
    for lines in fo:
        line=lines.split(" ")
        if len(line)==16 and j!=21:
           print(line)
           line[13]=str(1-float(line[5])).ljust(4,'0')
           line[15]=str(1./(num_tasks-1.))+"\n"
           fw.writelines(' '.join(line))
           print(line)
        elif len(line)==16 and j==21:
           print(line)
           line[13]=str(1-float(line[5])).ljust(4,'0')
           line[15]=str(0.02)+"\n"
           fw.writelines(' '.join(line))
           print(line)
        else:
           fw.writelines(' '.join(line))
    fw.close()
    fo.close()
