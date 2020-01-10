#!/usr/bin/env python2
import subprocess
import os
import sys
import time
import math
import numpy as np
import uuid
import zipfile
import shutil
sys.path.insert(0, "/home/dibyendu92/THROMBIN/python_scripts2/replica_copy")  
import make_check_file
import make_check_bash
import worker_check_new
import parser
import argparse
import make_run_bash
import worker_run_new

#ARGUMENTS
parse = argparse.ArgumentParser()
parse.add_argument("replica", help="number of replica runs (not swaps)", type=int)
parse.add_argument("swaps", help="number of swaps", type=int)

args = parse.parse_args()

file_path= os.path.abspath(".")+"/"
num_tasks = args.replica                                                 # total number of frames in the serial run; should be equal to the number comes after map_lambda in start_input file 
num_tasks1 = args.replica                                                 # should be same as num_tasks
num_tasks2 = args.replica                                                 # should be same as num_tasks
lambda_decre = float(1.0/(num_tasks-1))
start_input="2zf0_ac_start.inp"                                 # name of the input file for 1st serial run, please read the MAKE_INPUT file to know how to make the input file 
check_input = "2zf0_ac_check.inp"                               # name of the demo input file for checking runs, please read the MAKE_INPUT file to know how to make the input file
run_input = "2zf0_ac_run.inp"                                   # name of the demo input file for parallel runs, please read the MAKE_INPUT file to know how to make the input file
restart_folder=file_path+"output/"+start_input.split(".")[0]+"/"                                 # path of the folder from which, we get the restart files after the 1st serial run 
shell_script_check= file_path + 'parallel_check.bash'           # complete path of the bash script for check runs
shell_script_run= file_path + 'parallel_run.bash'               # complete path of the bash script for parallel runs

subprocess.call([file_path + 'start.bash', '', ''])             # 'start.bash' is used to submit the 1st serial run
for i in range(1,args.swaps+1):
    counter = i                                                 # counter (number of times the loop is running)
    if i>1:
       job_type='parallel'
       print 'Now Running Parallel Job'
       subprocess.call([file_path +'copy_res.bash', '', ''])    # 'copy_res.bash' is used to copy all restart files(after all parallel run)to the current dir(see comments in 'copy_res.bash')
    else:
       job_type='serial'
       print 'Now Running Serial Job'
       for j in range(1,args.replica+1):
           shutil.copy(restart_folder+"ac.res"+"%03d" %j, file_path)             # copy all restart files(only after serial run)from the path given in 'restart_folder' to the current dir
    make_check_file.make_check(counter, num_tasks, lambda_decre, check_input)    # the func 'make_check' takes two arguments.This step generates ac_0XX.inp;acswap_0XX.inp. (you should not modify this line) 
    make_check_bash.check_bash(num_tasks)                                        # you need 'parallel_check_demo.bash'(don't change the name of the script) file in your working directory for this step. 
    print "Checking Files Were Made"                                             # you should see a file 'parallel_check.bash' after this step.
    if worker_check_new.parallel_check_mode(shell_script_check,num_tasks1,num_tasks2,subprocess,time):       # 'parallel_check_mode' takes 5 args(maintain the order), (donot change this line)
       print "Checking Is Finished\n"                                                                          # 'ac_0XX.out', and 'acswap_0XX.out' are generated; zero stepped checking jobs
       print 'Currently on Swap ' + str(i) + '/' + str(args.swaps)
       parser.parse_file(counter, num_tasks, lambda_decre, run_input, sys, math, np)                           # (donot change the line) maintain the argument ordering. Makes acrun_0XX.inp for actual runs 
       print "Parsing Is Completed"                                
       make_run_bash.run_bash(num_tasks)                                         # you need 'parallel_run_demo.bash'(don't change the name of the script)file in your working directory for this step.                        
       if worker_run_new.parallel_run_mode(shell_script_run,num_tasks,subprocess,time):                      # 'parallel_run_mode' takes 4 args(maintain the order), (donot change this line)
          print "Parallel Jobs Are Finished"                                                                 # 'acrun_0XX.out' are generated; 20000 steps run (see worker_run.py to change anything in this line)
          folder_name='tmp-' + str(uuid.uuid4()) + '%03d' %i                                                 # 'folder_name' generates a .zip file after completion of the set of parallel runs
          src_files = os.listdir(".")                              
          zf=zipfile.ZipFile("%s.zip" % (folder_name), "w", zipfile.ZIP_DEFLATED)
          for file_name in src_files:
              full_file_name = os.path.join(".", file_name)
              if (os.path.isfile(full_file_name)):
                  if file_name.split(".")[0] == "ac" or file_name.split(".")[1] == "out":                    # don't change these lines if you haven't change the name of 
                    if file_name.split("_")[0] == "acrun" or file_name.split(".")[0] == "ac":                # the restart(ac.res0XX.res) or input(acrun_0XX.inp)files for parallel runs
                       abs_src = os.path.abspath(".")
                       absname = os.path.abspath(full_file_name)
                       arcname = absname[len(abs_src) + 1:]
                       zf.write(full_file_name, arcname)
                       os.remove(full_file_name)
          zf.close()
       print "Its Working"
