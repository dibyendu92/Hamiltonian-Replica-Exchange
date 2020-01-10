#!/usr/bin/env python2


def check_completion(out_file,flag):
   """ description: Check if the run is completed and completed normally and then 
                    extract the potential energy after a certain step

                    out_file: is the name of the output file
                    flag: True or False; if True then the run is a production run
                                            False then the run is a checking run
                                            We run a 2ps (1000*0.002) production before 
                                            any subsequent swap
                                            In checking step we collect the potential energy
                                            to decide whether we should perform a exhance or 
                                            not
   """
   import sys
    
 #  import uuid

   # if flag=True then pattern_step=pattern_run
   # else  pattern_step=pattern_check
   # sample      'Energies for the system at step         10:' #9 spaces
   # sample      'Energies for the system at step        360:' #8 spaces 
   # sample      'Energies for the system at step       1570:' #7 spaces
   pattern_check='Energies for the system at step          0:'
   pattern_run='Energies for the system at step       1000:'
   pattern_check=pattern_check.split()
   pattern_run=pattern_run.split()
   job_checker= 'Peak memory usage during the run:'
   job_checker=job_checker.split()
   job_kill='The program received a STOP signal in routine:'
   job_kill=job_kill.split()
   if flag:
      pattern_step=pattern_run
   else:
      pattern_step=pattern_check

   pattern_epot=' system  - epot'
   pattern_epot=pattern_epot.split(" ")

   start_searching=False
   search_final=False

#   print '\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',out_file,'\n'

   loop_status=True
   success=False

   with open(out_file,'r') as infile:
        for line in infile:
            if loop_status:
               tmp_1=line.split()
               tmp_2=line.split(" ")
               if tmp_1==job_kill:
                  sys.exit(1)
               else:
                  if len(tmp_1)>6 and tmp_1[0:7]==pattern_step[0:7]:
                     start_searching=True
                  if start_searching:
                     if pattern_epot==tmp_2[0:5]:
                        search_final=True
                     if tmp_1==job_checker and search_final:
                        success=True
                        loop_status=False

#   print 'Exit status:',start_searching,search_final

   return success

#print check_completion('ac_001.out',0)

#if __name__ == "__main__":
#     check_completion(out_file,flag)
