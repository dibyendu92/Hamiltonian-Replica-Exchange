import argparse
import subprocess
import numpy as np
import os
import sys
import os.path
import time

#Last updated 09/09/18
# Code written by Jacob Florian and modified by Dibyendu Mondal
# This script runs adiabatic charging calculations for ligands in thrombin protein
# Example (rex): python run_rex_v5.py --replicas 11 --steps 2000 --swap 100 --serial 200 --type CF3 --decharge NO 
# For serial run, set --swap 0 and --serial to the number of steps 
# Example (serial): python run_rex_v5.py --replicas 11 --steps 100 --swap 0 --serial 20000 --type CL --decharge YES
# Uses main_script_v4.py for mapping and running molaris
main_dir = os.getcwd()

#ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--replicas", help="number of replica runs (not swaps)", type=int) #BETWEEN 1 AND 24 REPLICAS; MUST BE ODD NUMBER
parser.add_argument("--steps", help="number of steps per replica", type=int) #BETWEEN 10 AND 100000 STEPS; INCREMENTS OF 10
parser.add_argument("--serial", help="number of steps per lambda increment in the serial run", type=int) 
parser.add_argument("--swap", help="number of times replicas are swapped", type=int) #GREATER THAN 2
parser.add_argument("--type",help="type of run: CH3, CF3, NH2, CL, CL2", type=str)
parser.add_argument("--decharge",help="Whether decharging step is already completed", type=str) # --decharge YES or NO


args = parser.parse_args()

group = args.type
 
#PARAMETERS <==== Update these before starting
################################################################
################################################################
#File Names, these should stay the same
start_file_name = '2zf0_ac_start.inp'
check_file_name = '2zf0_ac_check.inp'
run_file_name = '2zf0_ac_run.inp'
starting_rest_in = 'ac_plus_4m.res'
main_script = 'main_script_v4.py'
start_file = 'start.bash'
copy_for_next_run = 'copy_for_next_run.bash'
copy_res = 'copy_res.bash'
pdb_file = '2CH3_plus_4m.pdb'
parallel_file1 = 'parallel_run.bash'
parallel_file2 = 'parallel_run_demo.bash'
parallel_file3 = 'parallel_check.bash'
parallel_file4 = 'parallel_check_demo.bash'
gen_map_file = 'gen_map.bash'
mod_gap_file = 'mod_gap.py'
mapping_file = 'map_ac.inp'
#proc_file = 'proc.py'

python_scripts_path = '/home/dibyendu92/THROMBIN/python_scripts2/replica_copy'
required_files = [starting_rest_in, start_file_name, check_file_name, run_file_name, main_script, start_file, copy_for_next_run, copy_res, pdb_file, parallel_file4, parallel_file3, parallel_file2, parallel_file1, gen_map_file, mod_gap_file, mapping_file]

#If these are changed, also change set_vdw and set_vdw_recharge functions
reg1_atm = '4144 to 4149 4154 to 4154 4188 to 4191 4195 to 4200' 
reg1_charge_list = [4144, 4145, 4146, 4147, 4148, 4149, 4154, 4188, 4189, 4190, 4191, 4195, 4196, 4197, 4198, 4199, 4200]
reg1_atm_list = np.arange(4144, 4202)

#Match the charges with reg1_atm_list (ie. CH3_charges[1] goes with reg1_atm_list[1])
CH3_charges = [-0.232, 0.078, -0.349, 0.324, -0.283, -0.109, 0.147, -0.469, 0.457, -0.575, -0.448, 0.145, -0.224, 0.051, -0.010, -0.037, 0.450, -0.591, 0.219, -0.231, 0.178, -0.246, -0.073, -0.173, -0.091, -0.230, -0.609, 0.087, 0.100, 0.115, 0.155, 0.161, 0.134, 0.131, 0.142, 0.036, 0.037, 0.028, 0.038, 0.035, 0.059, 0.036, 0.039, 0.054, 0.179, 0.156, 0.139,  0.156, 0.414, 0.383, 0.331, 0.128, 0.124, 0.126, 0.000, 0.000, 0.000, 0.407]
CL2_charges = [-0.011, 0.191, -0.165, -0.022, -0.012, -0.181, -0.125, -0.324, 0.378, -0.562, -0.115, 0.310, -0.206, -0.112, 0.100, -0.123, 0.322, -0.553, 0.251, -0.243, 0.154, -0.211, -0.105, -0.143, -0.114, -0.209, -0.494, 0.085, 0.099, 0.119, 0.152, 0.161, 0.137, 0.136, 0.137, 0.010, 0.042, 0.040, 0.020, 0.014, 0.115, 0.074, 0.117, 0.104, 0.160, 0.131, 0.166, -0.095, 0.380, 0.360, 0.281, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.375]
CH32_charges = [0.228, -0.093, -0.287, 0.262, -0.285, -0.266, 0.054, -0.394, 0.393, -0.595, -0.365, 0.350, -0.222, -0.022, 0.097, -0.167, 0.349, -0.575, 0.302, -0.328, 0.228, -0.259, -0.055, -0.188, -0.096, -0.230, -0.550, 0.074, 0.121, 0.128, 0.153, 0.163, 0.136, 0.126, 0.146, -0.002, 0.048, 0.058, 0.017, 0.007, 0.074, 0.049, 0.072, 0.088, 0.171, 0.172, 0.169, -0.360, 0.398, 0.364, 0.306, 0.107, 0.106, 0.104, 0.101, 0.110, 0.118, 0.389]
CH3_CL_charges = [0.271, -0.106, -0.024, -0.091, 0.044, -0.403, -0.041, -0.353, 0.432, -0.599, -0.135, 0.256, -0.151, 0.009, 0.061, -0.118, 0.258, -0.553, 0.343, -0.324, 0.241, -0.278, -0.058, -0.170, -0.102, -0.246, -0.567, 0.061, 0.120, 0.126, 0.159, 0.173, 0.139, 0.127, 0.141, 0.017, 0.043, 0.048, 0.021, 0.015, 0.060, 0.044, 0.091, 0.115, 0.131, 0.119, 0.203, -0.306, 0.398, 0.373, 0.292, 0.000, 0.000, 0.000, 0.092, 0.099, 0.108, 0.395]
################################################################
#PARAMETER CHECKS
if args.replicas % 2 == 0:
        print('Error: Number of replicas must be an odd number')
        sys.exit()
if args.steps > 99990 or args.steps < 10:
        print('Error: Number of steps/swap must be between 10 and 100000')
        sys.exit()
if args.steps % 10 != 0:
        print('Error: Number of steps/swap must be divisible by 10')
        sys.exit()
if args.replicas > 24 or args.replicas < 3:
        print('Error: Number of replicas must be between 3 and 24 (max # of processors)')
        sys.exit()
if args.type != '2CH3' and args.type != 'CL2' and args.type != 'CH3' and args.type != 'CH3CL':  
        print('Error: Type must be either 2CH3, CH3CL, or CH3')
        sys.exit()

#CHECK IF WE HAVE ALL REQUIRED FILES
for i in required_files:
        if not os.path.isfile(i):
                print(('Error: ' + i + ' does not exist'))
                sys.exit()

#FUNCTIONS
def replace_line(file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()

def append_line(file_name, line_num, phrase):
        f = open(file_name, "r")
        contents = f.readlines()
        f.close()
        contents.insert(line_num + 1, phrase)
        f = open(file_name, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

def get_line_number(file_name, phrase):
        lines = open(file_name, 'r').readlines()
        for i in range(len(lines)):
                line = lines[i].strip(' ')
                if line.startswith(phrase):
                        return i
        print(('Error: ' + phrase + ' does not exist in ' + file_name))

def set_charges_init(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] not in reg1_charge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH32_charges[i]) + ' ' + str(CH32_charges[i]) + '\n')
                else:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH32_charges[i]) + ' 0.0\n')

def set_charges_0(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] not in reg1_charge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH32_charges[i]) + ' ' + str(CH32_charges[i]) + '\n')
                else:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' 0.0 0.0\n')


def recharge(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        if args.type == 'CH3':
                charge_list = CH3_charges
        elif args.type == '2CH3':
                charge_list = CH32_charges
        elif args.type == 'CH3CL':
                charge_list = CH3_CL_charges
        elif args.type == 'CL2':
                charge_list = CL2_charges

        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] not in reg1_charge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH32_charges[i]) + ' ' + str(charge_list[i]) + '\n')
                else:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' 0.0 ' + str(charge_list[i]) + '\n')


def set_vdw_1(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        if args.type == 'CH3':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4198 to 4200\n')
                append_line(file_name, line_num, '    ab_vdw 4198 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4199 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4200 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4191 C4 H1\n')
        elif args.type == 'CH3CL':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4195 to 4197\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4197 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4154 C4 CL\n')
        elif args.type == 'CL2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4195 to 4200\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4197 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4198 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4199 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4200 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4154 C4 CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 C4 CL\n')

def set_vdw_recharge(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        if args.type == 'CH3':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4198 to 4200\n')
                append_line(file_name, line_num, '    ab_vdw 4191 H1 H1\n')
                append_line(file_name, line_num, '    ab_vdw 4198 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4199 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4200 DY DY\n')
        elif args.type == 'CH3CL':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4195 to 4197\n')
                append_line(file_name, line_num, '    ab_vdw 4154 CL CL\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4197 DY DY\n')
        elif args.type == 'CL2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4195 to 4200\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4197 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4198 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4199 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4200 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4154 CL CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 CL CL\n')



def mkdir(directory):
        if not os.path.exists(directory):
                os.makedirs(directory)

def cp_files_to_current_directory():
        for f in required_files:
                subprocess.call(['cp', main_dir + '/' + f, '.'])

def new_folder(name):
        os.chdir(main_dir)
        mkdir(name)
        os.chdir(name)
        cp_files_to_current_directory()

#ARGUMENT VARIABLES
steps = str(args.steps)
replicas = str(args.replicas)
swaps = str(args.swap)
num_tasks = args.replicas

print('\n')
print('=======================================================================')
print('============================STARING NEW RUN============================')
print(('============================ -CH3 to -' + args.type + ' ============================='))
print('=======================================================================')
print('\n')
print(('Number of Replicas: ' + replicas))
print(('Number of Swaps: ' + swaps))
print(('Number of Steps/Swaps: ' + steps))
print(('Number of Steps (Serial Run): ' + str(args.serial) + ' Steps * ' + replicas + ' Replicas'))
print(('Lambda Decrement: ' + str(float(1.0/(num_tasks-1)))))

#UPDATE pdb file name in start, run, and check files
replace_line(start_file_name, 0, pdb_file + ' keeph\n')
replace_line(run_file_name, 0, pdb_file + ' keeph\n')
replace_line(check_file_name, 0, pdb_file + ' keeph\n')

#UPDATE map_pf keyword in start file
line_num = get_line_number(start_file_name, 'map_pf')
replace_line(start_file_name, line_num, '    map_pf ' + str(args.replicas) + ' 1 2\n')

#UPDATE reg1_atm in start, run, and check input files
line_num = get_line_number(start_file_name, 'reg1_res')
replace_line(start_file_name, line_num, '    reg1_res 259\n')

line_num = get_line_number(check_file_name, 'reg1_res')
replace_line(check_file_name, line_num, '    reg1_res 259\n')

line_num = get_line_number(run_file_name, 'reg1_res')
replace_line(run_file_name, line_num, '    reg1_res 259\n')

#UPDATE nsteps per replica in run file and serial run step size
line_num = get_line_number(start_file_name, 'nsteps')
replace_line(start_file_name, line_num, '          nsteps ' + str(args.serial) + '\n')

line_num = get_line_number(run_file_name, 'nsteps')
replace_line(run_file_name, line_num, '          nsteps ' + str(args.steps) + '\n')

#UPDATE initial restart file in start file
line_num = get_line_number(start_file_name, 'rest_in')
replace_line(start_file_name, line_num, '    rest_in ' + starting_rest_in + '\n')

#UPDATE job_check_new with correct steps per replica
os.chdir(python_scripts_path)
line_num = get_line_number('job_check_new.py', "pattern_run='Energies for the system at step")

if len(steps) == 2:
        replace_line('job_check_new.py', line_num, "   pattern_run='Energies for the system at step         " + steps + ":'" + '\n')
elif len(steps) == 3:
        replace_line('job_check_new.py', line_num, "   pattern_run='Energies for the system at step        " + steps + ":'" + '\n')
elif len(steps) == 4:
        replace_line('job_check_new.py', line_num, "   pattern_run='Energies for the system at step       " + steps + ":'" + '\n')
elif len(steps) == 5:
        replace_line('job_check_new.py', line_num, "   pattern_run='Energies for the system at step      " + steps + ":'" + '\n')

#UPDATE copy_res.bash with correct number of replicas
os.chdir(main_dir)
line_num = get_line_number(copy_res, 'for i in {1..')
replace_line(copy_res, line_num, 'for i in {1..' + replicas + '}\n')

#UPDATE the gen_map.bash script and make map folder
line_num = get_line_number(gen_map_file, 'for f in $(seq -f "%03g" 1')
replace_line(gen_map_file, line_num, 'for f in $(seq -f "%03g" 1 ' + replicas + ')\n')

#UPDATE mod_gap.py with correct number of replicas
line_num = get_line_number(mod_gap_file, 'num_tasks=')
replace_line(mod_gap_file, line_num, 'num_tasks=' + replicas + '\n')

line_num = get_line_number(mod_gap_file, 'if len(line)==16 and j!=')
replace_line(mod_gap_file, line_num, '        if len(line)==16 and j!=' + replicas +':\n')

line_num = get_line_number(mod_gap_file, 'elif len(line)==16 and j==')
replace_line(mod_gap_file, line_num, '        elif len(line)==16 and j==' + replicas +':\n')

#UPDATE the map_ac.inp file with correct number of replicas
line_num = get_line_number(mapping_file, 'map_pf')
replace_line(mapping_file, line_num, 'map_pf ' + replicas + ' 1 2\n')

line_num = get_line_number(mapping_file, 'fileroot ./map_ac.gap')
replace_line(mapping_file, line_num, 'fileroot ./map_ac.gap ' + replicas + '\n')

###############################Decharging Step#################################
print('\n')
print('=======================================================================')
print('========================STARING DECHARGING STEP========================')
print('=======================================================================')
print('\n')

#Make CH3_decharge directory and copy all files from main_dir

if args.decharge == 'NO':
        mkdir('CH3_decharge')
        os.chdir('CH3_decharge')
        cp_files_to_current_directory()

        #MODIFY INPUT FILES
        set_charges_init(start_file_name)
        set_charges_init(check_file_name)
        set_charges_init(run_file_name) 
        #RUN main_script_v1.py

        subprocess.call(['python', main_script, replicas, swaps])
        #Process output from decharging run
        print('\n')
        print('Processing Output')
        time.sleep(1)
        os.chdir(main_dir)
else:
        if len(replicas) == 1:
                file_prefix = '/ac.res00'
        elif len(replicas) == 2:
                file_prefix = '/ac.res0'
        elif len(replicas) == 3:
                file_prefix = '/ac.res'
        if args.swap == 0:
                res_file_path = main_dir + '/2CH3_decharge/output/2zf0_ac_start' + file_prefix + replicas
        else: 
                if len(replicas) == 1:
                        out_fol_prefix = '/2H3_decharge/output/acrun_00' 
                elif len(replicas) == 2:
                        out_fol_prefix = '/2CH3_decharge/output/acrun_0' 
                elif len(replicas) == 3:
                        out_fol_prefix = '/2CH3_decharge/output/acrun_' 

                res_file_path = main_dir + out_fol_prefix + replicas + file_prefix + replicas
        print(res_file_path)

        if os.path.isfile(res_file_path):
                print('RESTART FILE FROM DECHARGING STEP IS FOUND')
                print('DECHARGING STEP HAS ALREADY BEEN COMPLETED IN SOME OTHER PREVIOUS SIMULATIONS, NO NEED TO PERFORM HERE')
                print('PROCEEDING TO THE NEXT STEP')
        else:
                print('ERROR: RESTART FILE FROM DECHARGING STEP IS NOT FOUND, RUN DECHARGING STEP FIRST')
                sys.exit()
    
###############################vdW Step#################################
if args.type != '2CH3':

        print('\n')
        print('=======================================================================')
        print('============================STARING VDW STEP 1=========================')
        print('=======================================================================')
        print('\n')
        
        #Make new vdw folder
        if args.type == 'CH3':
                new_folder('CH3_vdW')
                vdw_folder_name = 'CH3_vdW'
        elif args.type == 'CH3CL':
                new_folder('CH3CL_vdW')
                vdw_folder_name = 'CH3CL_vdW'
        elif args.type == 'CL2':
                new_folder('CL2_vdW')
                vdw_folder_name = 'CL2_vdW'

        #Get restart file from decharge output (If swap == 0, this is a serial run; else it is rex)
        if args.swap == 0:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        else:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_00' + replicas + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_0' + replicas + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_' + replicas + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        
        #Modify Input Files
        set_vdw_1(start_file_name)
        set_vdw_1(run_file_name)
        set_vdw_1(check_file_name)
        set_charges_0(start_file_name)
        set_charges_0(run_file_name)
        set_charges_0(check_file_name)

        #Run REX script
        subprocess.call(['python', main_script, replicas, swaps])
        
        time.sleep(1)
        os.chdir(main_dir)

###############################Recharging Step#################################
print('\n')
print('=======================================================================')
print('========================STARING RECHARGING STEP========================')
print('=======================================================================')
print('\n')

if args.type == 'CH3':
        new_folder('CH3_recharge')
elif args.type == 'CH3CL':
        new_folder('CH3CL_recharge')
elif args.type == 'CL2':
        new_folder('CL2_recharge')
elif args.type == '2CH3':
        new_folder('2CH3_recharge')

        #Get restart file from decharge output (If swap == 0, this is a serial run; else it is rex)
        if args.swap == 0:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/2zf0_ac_start' + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        else:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_00' + replicas + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_0' + replicas + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/2CH3_decharge/output/acrun_' + replicas + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])

if args.type != '2CH3':

        #Get restart file from vdW output
        if args.swap == 0:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/2zf0_ac_start' + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/2zf0_ac_start' + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/2zf0_ac_start' + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        else:   
                #Get restart file from vdw output
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/acrun_00' + replicas + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/acrun_0' + replicas + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/' + vdw_folder_name + '/output/acrun_' + replicas + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])

#Modify input files
set_vdw_recharge(start_file_name)
set_vdw_recharge(run_file_name)
set_vdw_recharge(check_file_name)
recharge(start_file_name)
recharge(run_file_name)
recharge(check_file_name)

#Run main script
subprocess.call(['python', main_script, replicas, swaps])

time.sleep(1)

print('All Done')
        





