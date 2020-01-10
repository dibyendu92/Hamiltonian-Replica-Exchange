#!/usr/bin/env python2


def parallel_run_mode(shell_script,num_tasks):
   """description This script check whether the real production jobs are finished or not
      
      shell_script_check: name of the shell script to run the jobs
      num_tasks: num of replica windows; number of parallel jobs"""

   import subprocess
   import time
   from job_check_new import check_completion
 
 
   check=[0 for i in range(num_tasks)]

   out_file_prefix='acrun_'
   out_file_suffix='.out'

   status=False
   
   subprocess.Popen([shell_script, '', ''])

   while True:

      time.sleep(1)

 #     print '\n\n'

      for i in range(1,num_tasks+1):
 #        print 'In advance:',check,'\n'
         current="%03d" % i
#         print '\nChecking the file: '+out_file_prefix+current+out_file_suffix+' ...'
         check[i-1]=check_completion(out_file_prefix+current+out_file_suffix,1)
#         print 'Result of the check:',check[i-1]
#         print 'After the check:',check,'\n'


      if sum(check)==num_tasks:
         status=True
         break

   return status


#shell_script='/home/dibyendu92/project/dmondal/proj-2/fep/methyl/half/rem/final/parallel_run.bash'

#num_tasks=21


#print parallel_worker(shell_script,num_tasks)

#if __name__ == "__main__":
#     import subprocess
#     import time
#     parallel_run_mode(shell_script,num_tasks,subprocess,time)
