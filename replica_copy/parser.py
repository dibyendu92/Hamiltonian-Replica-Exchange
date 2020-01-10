#!/usr/bin/env python2
def parse_file(x, num_tasks, lambda_decre, run_input):
    """ description: Parse molaris output file to extract the potential energy of 
                      of the system and decide whether the swaps between the 
                      replicas are allowed or not, based on the metropolis
                      hastings criterion
                      1. If the calculated boltzmann probability is less then onw, then
                      it would be called conditional acceptance or rejection 
                      2. If the energy difference of the system after exchange is negative
                      then it should be unconditional acceptance
                      
                      temperature of the simulation system is hard coded as 300 K
                      please follow the reference for further clarification
                      
                      (https://pubs.acs.org/doi/abs/10.1021/acs.jpcb.9b07593)
 
                     x: a number to denote even or odd round of swapping cycle 
             num_tasks: total number of windows
          lambda_decre: fraction of lambda that decreases 
                        from current window to the next one
             run_input: name of the demo input file
          Note: Please read MAKE_INPUT file to know how to make demo input file 
          '2zf0_ac_run.inp' for this script."""

    import sys
    import numpy as np
    import math
    import ini_odd_switch
    import ini_even_switch
    import no_switch

    file_original=[]
    file_swap=[]
    initial=1                                                  # initial frame number 
    final=int(num_tasks) + 1                                                   # final frame number + 1

   # sample      'Energies for the system at step         10:' #9 spaces
   # sample      'Energies for the system at step        360:' #8 spaces 
   # sample      'Energies for the system at step       1570:' #7 spaces

    for i in range(initial,final):
            file_original.append("ac_"+"%03d" %i+".out")       # generated from check runs, ac_0XX.inp contains same restart file ac.res0XX
            file_swap.append("acswap_"+"%03d" %i+".out")       # generated from check runs, acswap_0XX.inp contains restart from adjacent run

    pattern_step='Energies for the system at step          0:'

    pattern_step=pattern_step.split(':')[0].split()

    pattern_epot=' system  - epot'
    pattern_epot=pattern_epot.split(" ")
    epot_original={}                                            # Potential energy of the system non-switched runs 
    epot_swap={}                                                # Potential energy of the system switched runs

    start_searching=False

    RT=0.593                                                    # RT expressed in kcal/mol T is 300K

    for i in range(initial,final):
        with open(file_original[i-1],'r') as infile:
             for line in infile:
                 tmp_1=line.split()
                 if len(tmp_1)>6 and tmp_1[0:6]==pattern_step[0:6]:
                     start_searching=True                        
                 if start_searching:
                    if len(tmp_1)>9 and tmp_1[0]=='system' and line[0:21]==' system  - epot     :':
                          epot_original[i]=float(line[21:31])
                          start_searching=False
    print(epot_original)
    for i in range(initial,final):
         with open(file_swap[i-1],'r') as infile:
              for line in infile:
                  tmp_1=line.split()
                  if len(tmp_1)>6 and tmp_1[0:6]==pattern_step[0:6]:
                     start_searching=True
                  if start_searching:
                     if len(tmp_1)>9 and tmp_1[0]=='system'and line[0:21]==' system  - epot     :':
                           epot_swap[i]=float(line[21:31])
                           start_searching=False
    print(epot_swap)

#sys.exit(1)

    if x%2!=0:                                                     
       if len(epot_original)==len(epot_swap):
          no_switch.no_sw(final-1, final-1, lambda_decre, run_input)
          print("Should not be exchanged", final-1, "\n")
          for i in range (1,len(epot_original),2):
              delta=-(epot_original[i]+epot_original[i+1]-epot_swap[i]-epot_swap[i+1])/RT
              accepted=False

              if delta<0:
                 ini_odd_switch.odd_sw(i, i+1, lambda_decre, run_input, sys)
                 accepted=True
                 print('Unconditionally accepted [Delta]:',delta, "exchange between", i, "and", i+1, "\n")
              elif delta<11.0:
                   p=math.exp(-delta)
                   rnd=np.random.rand()
                   if p>rnd:
                      ini_odd_switch.odd_sw(i, i+1, lambda_decre, run_input, sys)
                      accepted=True
                      print('Conditionally accepted [P,r]:',p,rnd , "..", "exchange between", i, "and", i+1, "\n")
                   else:
                       no_switch.no_sw(i, i+1, lambda_decre, run_input)
                       print('No acceptance [P, r]:', p, rnd, "..", "exchange attempted", i, "and", i+1, "\n")
       else:
           sys.exit(1)  
    else:
        if len(epot_original)==len(epot_swap):
           no_switch.no_sw(initial, initial, lambda_decre, run_input)
           print("Should not be exchanged", initial, "\n")
           for i in range (len(epot_original),1,-2):
               delta=-(epot_original[i]+epot_original[i-1]-epot_swap[i]-epot_swap[i-1])/RT

               accepted=False

               if delta<0:
                  ini_even_switch.even_sw(i-1, i, lambda_decre, run_input, sys)
                  accepted=True
                  print('Unconditionally accepted [Delta]:', delta, "exchange between", i-1, "and", i, "\n")
               elif delta<11.0:
                    p=math.exp(-delta)
                    rnd=np.random.rand()
                    if p>rnd:
                       ini_even_switch.even_sw(i-1, i, lambda_decre, run_input, sys)
                       accepted=True
                       print('Conditionally accepted [P,r]:', p, rnd ,"..", "exchange between", i-1, "and", i, "\n")
                    else:
                        no_switch.no_sw(i-1, i, lambda_decre, run_input)
                        print('No acceptance [P, r]:', p, rnd, "..", "exchange attempted", i-1, "and", i, "\n")
        else:
            sys.exit(1)
## This script extracts potential energies of the system from the check-run output files. The check-runs are MDrun for '0' steps. It then makes
## two dictionary a)epot_original, and b)epot_swap. Then it use the Metropolis-Hasting algorithm to check whether an exchange attempt is
## possible or not. uses no_switch, ini_even_switch, ini_odd_switch python scripts to generate input files 'acrun_0XX.inp' for parallel runs.  
## when counter(x) in 'main_script.py' is odd, attempts are made to switch between window starting from odd number.

#if __name__=="__main__":
#     import sys
#     import math
#     import numpy as np
#     parse_file(x,run_input,sys,math,np)
