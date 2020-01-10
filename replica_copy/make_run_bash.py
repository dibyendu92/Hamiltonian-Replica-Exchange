#!/usr/bin/env python

def run_bash(num_tasks):
    """ """ Description: Generates a bash file named "parallel_run.bash" to run MD simulations
                       
             num_tasks: number of simulations to run
    """
    initial = 1
    final = int(num_tasks) + 1
    with open('parallel_run_demo.bash','r') as inputfile:
         out_file=open('parallel_run.bash','w')
         for lines in inputfile:
             line=lines.split()
             if len(line)> 3 and line[1]=="acrun_0XX.inp":
                for i in range(initial, final):
                    line[1]="acrun_" + "%03d" %i + ".inp"
                    line[3]="acrun_" + "%03d" %i + ".out"
                    out_file.writelines(" ".join(line)+ "\n")
             else:
                    out_file.write(lines)
    out_file.close()

## This scirpt will make a bash script 'parallel_run.bash' from a demo bash script 'parallel_run_demo.bash' (should be in the current working
## directory) to run parallel molaris jobs.

#if __name__ == "__main__":
#     run_bash() 
