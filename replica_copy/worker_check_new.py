#!/usr/bin/env python2


def parallel_check_mode(shell_script_check,num_tasks1,num_tasks2):
   """description This script check whether the check jobs are finished or not
      
      shell_script_check: name of the shell script to run the jobs
      num_tasks1: num of replica windows; number of parallel jobs
      num_tasks2: num of replica windows; number of parallel jobs after swaps"""

   import subprocess
   import time
   from job_check_new import check_completion

   check1=[0 for i in range(num_tasks1)]
   check2=[0 for i in range(num_tasks2)]
   out_file1_prefix='ac_'
   out_file2_prefix='acswap_'
   out_file_suffix='.out'
   check=check1+check2
   status=False

   subprocess.Popen([shell_script_check, '', ''])

   while True:

      time.sleep(1)

      for i in range(1,num_tasks2+1):
         current="%03d" % i
         check1[i-1]=check_completion(out_file1_prefix+current+out_file_suffix,0)
         check2[i-1]=check_completion(out_file2_prefix+current+out_file_suffix,0)
      
      if sum(check1)==num_tasks1 and sum(check2)==num_tasks2:
         status=True
         break

   return status


#if __name__ == "__main__":
#     import subporcess
#     import time
#     parallel_check_mode(shell_script_check,num_tasks1,num_tasks2,subprocess,time)
