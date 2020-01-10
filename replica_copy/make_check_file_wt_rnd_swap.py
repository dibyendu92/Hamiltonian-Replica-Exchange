#!/usr/bin/env python
import gen_pair

def ran_swap_res(i, j, lambda_decre, res_file, check_input):
    """ Description : This a module to make random swaps to make check files for running 1 step potential energy calculation
                      for different windows
                   i, j: window number involved in swapping
                   lambda_decre: lambda decrement interval, this signifies how fast the density of the initial themodynamics state
                   should change
                   res_file: a list comatining the name of the restart file
                   check_input: name of a demo input file     
    """
    file_write1=open("acswap_"+"%03d" %i+".inp","w")
    file_write2=open("acswap_"+"%03d" %j+".inp","w")
    with open(check_input,"r") as inputfile:
         for lines in inputfile:
             line=lines.split(" ")
             if len(line)>5 and line[4]=="rest_in":
                   if i:
                      line[5]=res_file[j-1]+"\n"
                      file_write1.writelines(" ".join(line))
                   if j:
                      line[5]=res_file[i-1]+"\n"
                      file_write2.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="map_lambda":
                  if i:
                     line[5]=str(1-(i-1)*lambda_decre)+"\n"
                     file_write1.writelines(" ".join(line))
                  if j:
                     line[5]=str(1-(j-1)*lambda_decre)+"\n"
                     file_write2.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="rest_out":
                  if i:
                     line[5]=res_file[i-1]+"\n"
                     file_write1.writelines(" ".join(line))
                  if j:
                     line[5]=res_file[j-1]+"\n"
                     file_write2.writelines(" ".join(line))
             else:
                  file_write1.writelines(" ".join(line))
                  file_write2.writelines(" ".join(line))

    file_write1.close()
    file_write2.close()
    return
 
def no_swap(a, lambda_decre, res_file, check_input):
    """ Description : This a module to make check files with no swap for running 1 step potential energy calculation
                      for different windows
                   a: window number
                   lambda_decre: lambda decrement interval, this signifies how fast the density of the initial themodynamics state
                   should change
                   res_file: a list comatining the name of the restart file
                   check_input: name of a demo input file
    """

    file_write=open("acswap_"+"%03d" %a+".inp","w")
    with open(check_input,"r") as inputfile:
         for lines in inputfile:
             line=lines.split(" ")
             if len(line)>5 and line[4]=="rest_in":
                line[5]=res_file[a-1]+"\n"
                file_write.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="map_lambda":
                line[5]=str(1-(a-1)*lambda_decre)+"\n"
                file_write.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="rest_out":
                line[5]=res_file[a-1]+"\n"
                file_write.writelines(" ".join(line))
             else:
                file_write.writelines(" ".join(line))

    file_write.close()
    return  

def make_check(x, num_tasks, lambda_decre, comb_list, check_input):
    """ Description : This a module to make check files for running 1 step potential energy calculation
                      for different windows
                   x: step number for swapping 
                   when x is even, for a swapping pair (i,j) i should be an even number
                   when x is odd, for a swapping pair (i, j) i should be an odd number 
                   num_tasks: number of swapping windows of replicas involved  in swapping
                   lambda_decre: lambda decrement interval, this signifies how fast the density of the initial themodynamics state
                   should change
                   comb_list : a list of pairs of window numbers that are involved in swapping, only important for random swapping stage
                   The random swapping is performed after every 10 swap steps
                   check_input: name of a demo input file     
    """

#    import numpy as np
    initial=1
    final= int(num_tasks) + 1
    counter1=0
    lambda_value1=0
    res_file=[]
    output_file1=[]
    output_file2=[]  

 #   decrement_A = np.round(1.0/(final-2))
    # Check input file check_input=2zf0_ac_check.inp
    for i in range(initial,final):
        res_file.append("ac.res"+"%03d" %i)
        output_file1.append("ac_"+"%03d" %i+".inp")
    k=0
    for j in output_file1:
        file_write=open(j,"w")
        with open(check_input,"r") as inputfile:
             for lines in inputfile:
                 line=lines.split(" ")
                 if len(line)>5 and line[4]=="rest_in":
                    line[5]=res_file[counter1]+"\n"
                    counter1 +=1
                    file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="map_lambda":
                    line[5]=str(1-lambda_value1*lambda_decre)+"\n"
                    lambda_value1 +=1
                    file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="rest_out":
                    line[5]=res_file[k]+"\n"
                    file_write.writelines(" ".join(line))
                    k +=1
                 else:
                    file_write.writelines(" ".join(line))

        file_write.close()


    if x%2!=0 and x%5!=0:
       counter2=0
       lambda_value2=0
       for i in range(initial,final):
           output_file2.append("acswap_"+"%03d" %i+".inp")

       for j in range(initial,final):
           file_write=open(output_file2[j-1],"w")  
           with open(check_input,"r") as inputfile:
                for lines in inputfile:
                    line=lines.split(" ")
                    if len(line)>5 and line[4]=="rest_in":
                       if j%2!=0 and j!=final-1:
                          line[5]=res_file[counter2+1]+"\n"
                          counter2 +=1
                          file_write.writelines(" ".join(line))
                       elif j%2==0:
                          line[5]=res_file[counter2-1]+"\n"
                          counter2 +=1
                          file_write.writelines(" ".join(line))
                       else:
                          line[5]=res_file[j-1]+"\n"
                          file_write.writelines(" ".join(line)) 
                    elif len(line)>5 and line[4]=="map_lambda":
                       line[5]=str(1-lambda_value2*lambda_decre)+"\n"
                       lambda_value2 +=1
                       file_write.writelines(" ".join(line))
                    elif len(line)>5 and line[4]=="rest_out":
                       line[5]=res_file[j-1]+"\n"
                       file_write.writelines(" ".join(line))
                    else:
                       file_write.writelines(" ".join(line))

           file_write.close()
    elif x%2!=0 and x%5==0:
#        comb_list = gen_pair.gen_pair(initial, final-2)
        print comb_list
        for i,j in comb_list:
            ran_swap_res(i, j, lambda_decre, res_file, check_input)
        no_swap(final-1, lambda_decre, res_file, check_input)

    if x%2==0 and x%5!=0:
        counter2=0
        lambda_value2=0
        for i in range(initial,final):
           output_file2.append("acswap_"+"%03d" %i+".inp")

        for j in range(initial,final):
            file_write=open(output_file2[j-1],"w")
            with open(check_input,"r") as inputfile:
                 for lines in inputfile:
                     line=lines.split(" ")
                     if len(line)>5 and line[4]=="rest_in":
                        if j%2!=0 and j!=initial:
                           line[5]=res_file[counter2-1]+"\n"
                           counter2 +=1
                           file_write.writelines(" ".join(line))
                        elif j%2==0:
                           line[5]=res_file[counter2+1]+"\n"
                           counter2 +=1
                           file_write.writelines(" ".join(line))
                        else:
                           line[5]=res_file[j-1]+"\n"
                           counter2 +=1
                           file_write.writelines(" ".join(line))
                     elif len(line)>5 and line[4]=="map_lambda":
                          line[5]=str(1-lambda_value2*lambda_decre)+"\n"
                          lambda_value2 +=1
                          file_write.writelines(" ".join(line))
                     elif len(line)>5 and line[4]=="rest_out":
                         line[5]=res_file[j-1]+"\n"
                         file_write.writelines(" ".join(line))
                     else:
                          file_write.writelines(" ".join(line))

            file_write.close()
    elif x%2==0 and x%5==0:
#        comb_list = gen_pair.gen_pair(initial+1, final-1)
        print comb_list
        for i,j in comb_list:
            ran_swap_res(i, j, lambda_decre, res_file, check_input)
        no_swap(initial, lambda_decre, res_file, check_input)
       

#if __name__=="__main__":
#     make_check(x,check_input)
