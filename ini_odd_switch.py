#!/usr/bin/env python2
import sys
def odd_sw(x, y, lambda_decre, run_input, sys):
    """ description: Generates input file
                     The generated input file runs with swapped 
                     configurations (in odd swapping cycle xth(an odd
                     number) configuration is swapped with yth(x+1th) windows)
                     x: Initial window number
                     y: final window number
          lambda_decre: fraction of lambda that decreases 
                        from current window to the next one
             run_input: name of the demo input file"""

    initial=int(x)
    final=int(y)+1
    output_file2=[]
    res_file=[]
#initial=int(sys.argv[1])
#final=int(sys.argv[2])+1
# Run Input file run_input=2zf0_ac_run.inp
    lambda_value2=initial-1

    if initial%2 !=0 or initial==y:
       pass
    else:
       "odd_sw function should be used for switching configurations in odd rounds"
       "please check the first and the second arguments of the function"
       sys.exit(1)

    for i in range(initial,final):
        output_file2.append("acrun_"+"%03d" %i+".inp")
        res_file.append("ac.res" + "%03d" %i)
    k=0
    for j in range(initial,final):
        file_write=open(output_file2[k],"w")
        with open(run_input,"r") as inputfile:
             for lines in inputfile:
                 line=lines.split(" ")
                 if len(line)>5 and line[4]=="rest_in":
                    if j%2!=0 and j!=final-1:
                       line[5]=res_file[1] + "\n" 
                       file_write.writelines(" ".join(line))
                    elif j%2==0:
                       line[5]=res_file[0] + "\n"
                       file_write.writelines(" ".join(line))
                    else:
                       line[5]=res_file[0] + "\n"
                       file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="map_lambda":
                    line[5]=str(1-lambda_value2*lambda_decre)+"\n"
                    lambda_value2 +=1
                    file_write.writelines(" ".join(line))
                 elif len(line)>5 and line[4]=="rest_out":
                    line[5]=res_file[k]+"\n"
                    file_write.writelines(" ".join(line))
                    k +=1
                 elif len(line)>5 and line[4]=="energy_out":
                    line[5]="map_ac.gap" + "%03d" %j + "\n"
                    file_write.writelines(" ".join(line))
                 else:
                    file_write.writelines(" ".join(line))


        file_write.close()

#if __name__ == "__main__":
#     import sys
#     odd_sw(initial,final,run_input,sys)
