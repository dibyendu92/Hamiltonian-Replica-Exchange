#!/usr/bin/env python2
import sys
def random_sw(x, y, lambda_decre, run_input, sys):
    """ description: Generates input file
                     The generated input file runs with swapped 
                     configurations (random swapping between xth
                     and yth windows)
                     x: Initial window number
                     y: final window number
          lambda_decre: fraction of lambda that decreases 
                        from current window to the next one
             run_input: name of the demo input file"""

    initial=int(x)
    final=int(y)

    file_write1=open("acrun_"+"%03d" %x+".inp","w")
    file_write2=open("acrun_"+"%03d" %y+".inp","w")
    with open(run_input,"r") as inputfile:
         for lines in inputfile:
             line=lines.split(" ")
             if len(line)>5 and line[4]=="rest_in":
                   if x:
                      line[5]="ac.res" + "%03d" %y +"\n"
                      file_write1.writelines(" ".join(line))
                   if y:
                      line[5]="ac.res" + "%03d" %x +"\n"
                      file_write2.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="map_lambda":
                  if x:
                     line[5]=str(1-(x-1)*lambda_decre)+"\n"
                     file_write1.writelines(" ".join(line))
                  if y:
                     line[5]=str(1-(y-1)*lambda_decre)+"\n"
                     file_write2.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="rest_out":
                  if x:
                     line[5]="ac.res" + "%03d" %x +"\n"
                     file_write1.writelines(" ".join(line))
                  if y:
                     line[5]="ac.res" + "%03d" %y+"\n"
                     file_write2.writelines(" ".join(line))
             elif len(line)>5 and line[4]=="energy_out":
                      if x:
                         line[5]="map_ac.gap" + "%03d" %x + "\n"
                         file_write1.writelines(" ".join(line))
                      if y:
                         line[5]="map_ac.gap" + "%03d" %y + "\n"
                         file_write2.writelines(" ".join(line))           
             else:
                  file_write1.writelines(" ".join(line))
                  file_write2.writelines(" ".join(line))

    file_write1.close()
    file_write2.close()


#if __name__== "__main__":
#     import sys
#     even_sw(initial,final,run_input,sys)
