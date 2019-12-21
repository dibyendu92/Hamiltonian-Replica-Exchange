#!/usr/bin/env python
def check_bash(num_tasks):
    """ Description: Generates a bash file named "parallel_check.bash" to run 1 step energy calculations 
                     to get the potential energy of the start before and after swapping
                     num_tasks: number of simulations to run
    """
    initial = 1
    final = int(num_tasks) + 1
    with open('parallel_check_demo.bash','r') as inputfile:
         out_file=open('parallel_check.bash','w')
         for lines in inputfile:
             line=lines.split()
             if len(line)> 3 and line[1]=="ac_0XX.inp":
                for i in range(initial, final):
                    line[1]="ac_" + "%03d" %i + ".inp"
                    line[3]="ac_" + "%03d" %i + ".out"
                    out_file.writelines(" ".join(line)+ "\n")
             elif len(line)> 3 and line[1]=="acswap_0XX.inp":
                for i in range(initial, final):
                    line[1]="acswap_" + "%03d" %i + ".inp"
                    line[3]="acswap_" + "%03d" %i + ".out"
                    out_file.writelines(" ".join(line)+ "\n")
             else:
                    out_file.write(lines)
    out_file.close()
#if __name__=="__main__":
#     check_bash()
