#!/usr/bin/env python
#import sys
def no_sw(x, y, lambda_decre, run_input):
    """ description: Generates input file
                     The generated input file runs with non-swapped 
                     configurations

                     x: Initial window number
                     y: final window number
          lambda_decre: fraction of lambda that decreases 
                        from current window to the next one
             run_input: name of the demo input file
          Note: Please read MAKE_INPUT file to know how to make demo input file 
          '2zf0_ac_run.inp' for this script."""

    res_file=[]
    output_file=[]
    initial=int(x)
    final=int(y)+1
#initial=int(sys.argv[1])
#final=int(sys.argv[2])+1
#Start Input file run_input=2zf0_ac_run.inp
    lambda_value1=initial-1

    for i in range(initial,final):
        res_file.append("ac.res" + "%03d" %i)       #If the restart file name in molaris input file is not ac.res0XX, you have change this line
        output_file.append("acrun_"+"%03d" %i+".inp")
    k=0
    for j in output_file:
        file_write=open(j,"w")
        with open(run_input,"r") as inputfile:
             for lines in inputfile:
                 line=lines.split(" ")
                 if len(line)>5 and line[4]=="rest_in":
                    line[5]=res_file[k] + "\n"
                    file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="map_lambda":
                    line[5]=str(1-lambda_value1*0.03)+"\n"
                    lambda_value1 +=1
                    file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="rest_out":
                       line[5]=res_file[k]+"\n"
                       file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="energy_out":
                    line[5]="map_ac.gap" + res_file[k].split("res")[1]+ "\n"   #In demo input file 'enery_out' line should come after 'rest_in' 
                    file_write.writelines(" ".join(line))
                    k +=1
                 else:
                    file_write.writelines(" ".join(line))
        file_write.close()

## This script makes input file contains restart file generated from the same window/frame of MD run. For example acrun_004.inp will have restart 
## file generated from window/frame 4 (lambda value for state A is 0.85 for a 21 frame run) and acrun_005.inp will have
## ac.res005. Please read MAKE_INPUT file to know how to make demo input file '2zf0_ac_run.inp' for this script.


#if __name__== "__main__":
#     no_sw(initial,final,run_input)
