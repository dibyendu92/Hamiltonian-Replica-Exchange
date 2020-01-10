#import numpy as np

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]

protein = []
water = []
induced = []
intra = []
inter = []
vdw = []
born = []
lan=[]
c1 = []
c2 = []
total=[]

f = open('map_output.txt', 'r').readlines()

for line in f:
        if line.startswith('Protein         :'):
                temp = remove_prefix(line, 'Protein         :')
                temp2 = (temp.lstrip().rstrip())
                protein.append(float(temp2))
        elif line.startswith('Water           :'):
                temp = remove_prefix(line, 'Water           :')
                temp2 = (temp.lstrip().rstrip())
                water.append(float(temp2))
        elif line.startswith('Induced         :'):
                temp = remove_prefix(line, 'Induced         :')
                temp2 = (temp.lstrip().rstrip())
                induced.append(float(temp2))
        elif line.startswith('Intra           :'):
                temp = remove_prefix(line, 'Intra           :')
                temp2 = (temp.lstrip().rstrip())
                intra.append(float(temp2))
        elif line.startswith('Inter           :'):
                temp = remove_prefix(line, 'Inter           :')
                temp2 = (temp.lstrip().rstrip())
                inter.append(float(temp2))
        elif line.startswith('VDW             :'):
                temp = remove_prefix(line, 'VDW             :')
                temp2 = (temp.lstrip().rstrip())
                vdw.append(float(temp2))
        elif line.startswith('Born            :'):
                temp = remove_prefix(line, 'Born            :')
                temp2 = (temp.lstrip().rstrip())
                born.append(float(temp2))
        elif line.startswith('Langevin        :'):
                temp = remove_prefix(line, 'Langevin        :')
                temp2 = (temp.lstrip().rstrip())
                lan.append(float(temp2))
        elif line.startswith('Constraint I    :'):
                temp = remove_prefix(line, 'Constraint I    :')
                temp2 = (temp.lstrip().rstrip())
                c1.append(float(temp2))
        elif line.startswith('Constraint II   :'):
                temp = remove_prefix(line, 'Constraint II   :')
                temp2 = (temp.lstrip().rstrip())
                c2.append(float(temp2))

outFile = open('output.txt', 'w')

for i in range(len(protein)):
        total.append(protein[i] + water[i] + induced[i] +  inter[i] + vdw[i] + born[i] + lan[i] + c1[i] + c2[i])
        outFile.write(str('%.2f' %round(total[i], 2)))
        outFile.write('\n')     

outFile.close()


