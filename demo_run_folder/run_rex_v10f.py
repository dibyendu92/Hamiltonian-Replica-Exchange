import argparse
import subprocess
import numpy as np
import os
import sys
import os.path
import time

#Last updated 09/09/18
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
parser.add_argument("--type",help="type of run: CH3, CLF, BR, CL, F, H, CL2", type=str)
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
starting_rest_in = 'ac_plus_5m.res'
main_script = 'main_script_v4.py'
start_file = 'start.bash'
copy_for_next_run = 'copy_for_next_run.bash'
copy_res = 'copy_res.bash'
pdb_file = '2zf0_plus_5m.pdb'
parallel_file1 = 'parallel_run.bash'
parallel_file2 = 'parallel_run_demo.bash'
parallel_file3 = 'parallel_check.bash'
parallel_file4 = 'parallel_check_demo.bash'
gen_map_file = 'gen_map.bash'
mod_gap_file = 'mod_gap.py'
mapping_file = 'map_ac.inp'

python_scripts_path = '/home/dibyendu92/THROMBIN/python_scripts2/replica_copy'
required_files = [starting_rest_in, start_file_name, check_file_name, run_file_name, main_script, start_file, copy_for_next_run, copy_res, pdb_file, parallel_file4, parallel_file3, parallel_file2, parallel_file1, gen_map_file, mod_gap_file, mapping_file]

#If these are changed, also change set_vdw and set_vdw_recharge functions
reg1_atm = '4144 to 4198'
reg1_atm_list = np.arange(4144, 4199)
reg1_decharge_list = [4164, 4165, 4166, 4167, 4168, 4169, 4170, 4188, 4189, 4190, 4191, 4194, 4195, 4196]

#Match the charges with reg1_atm_list (ie. CH3_charges[1] goes with reg1_atm_list[1])
CH3_charges = [-0.609, 0.219, 0.450, -0.591, -0.231, 0.178, -0.230, -0.246, -0.091, -0.073, -0.173, -0.224, 0.145, 0.457, -0.575, -0.037, -0.010, 0.051, -0.469, 0.147, 0.078, -0.349, 0.324, -0.448, -0.283, -0.109, -0.231, 0.087, 0.100, 0.115, 0.155, 0.161, 0.134, 0.131, 0.142, 0.036, 0.037, 0.028, 0.038, 0.035, 0.059, 0.036, 0.039, 0.054, 0.179, 0.156, 0.139, 0.157, 0.414, 0.383, 0.128, 0.124, 0.126, 0.331, 0.407]
CLF_charges = [-0.695, 0.250, 0.467, -0.608, -0.219, 0.166, -0.215, -0.250, -0.095, -0.073, -0.174, -0.276, 0.313, 0.419, -0.566, -0.121, 0.118, -0.049, -0.467, 0.073, -0.119, -0.028, -0.126, -0.113, 0.078, -0.378, 0.384, 0.093, 0.099, 0.109, 0.152, 0.165, 0.135, 0.133, 0.145, 0.004, 0.042, 0.035, 0.015, -0.003, 0.099, 0.051, 0.083, 0.093, 0.147, 0.122, 0.211, -0.230, 0.433, 0.408, 0.0, 0.0, 0.0, 0.344, 0.430]
BR_charges = [-0.624, 0.296, 0.442, -0.598, -0.244, 0.171, -0.217, -0.230, -0.109, -0.083, -0.168, -0.185, 0.076, 0.518, -0.571, -0.042, 0.022, 0.013, -0.454, -0.167, 0.091, -0.029, -0.220, -0.082, 0.075, -0.230, -0.107, 0.056, 0.097, 0.115, 0.151, 0.154, 0.139, 0.134, 0.144, 0.049, 0.044, 0.027, 0.035, 0.021, 0.060, 0.051, 0.134, 0.142, 0.147, 0.106, 0.162, 0.135, 0.411, 0.378, 0.0, 0.0, 0.0, 0.342, 0.419]
CL_charges = [-0.601, 0.225, 0.420, -0.586, -0.233, 0.178, -0.224, -0.248, -0.090, -0.070, -0.181, -0.231, 0.149, 0.451, -0.565, -0.003, -0.033, 0.106, -0.456, 0.062, 0.088, -0.143, 0.019, -0.144, -0.053, -0.173, -0.179, 0.087, 0.101, 0.115, 0.154, 0.165, 0.134, 0.130, 0.145, 0.034, 0.029, 0.018, 0.038, 0.038, 0.046, 0.018, 0.075, 0.069, 0.142, 0.125, 0.158, 0.157, 0.411, 0.386, 0.0, 0.0, 0.0, 0.336, 0.405]
H_charges = [-0.561, 0.235, 0.334, -0.560, -0.265, 0.187, -0.228, -0.217, -0.111, -0.104, -0.153, -0.172, 0.244, 0.377, -0.560, -0.043, 0.069, -0.032, -0.387, 0.081, 0.114, -0.213, -0.121, 0.133, -0.140, -0.104, -0.214, 0.088, 0.109, 0.123, 0.156, 0.157, 0.139, 0.136, 0.141, 0.010, 0.026, 0.019, 0.019, 0.006, 0.073, 0.063, 0.048, 0.059, 0.150, 0.130, 0.127, 0.152, 0.400, 0.374, 0.0, 0.0, 0.0, 0.304, 0.399] 
F_charges = [-0.596, 0.215, 0.428, -0.591, -0.239, 0.178, -0.227, -0.225, -0.109, -0.093, -0.152, -0.229, 0.205, 0.452, -0.567, -0.072, 0.088, -0.003, -0.521, 0.258, 0.104, -0.398, 0.464, -0.280, -0.333, -0.048, -0.289, 0.090, 0.103, 0.116, 0.158, 0.159, 0.138, 0.134, 0.138, 0.024, 0.038, 0.026, 0.016, 0.003, 0.069, 0.049, 0.020, 0.027, 0.209, 0.192, 0.145, 0.177, 0.411, 0.383, 0.0, 0.0, 0.0, 0.348, 0.408]
CL2_charges = [-0.494, 0.251, 0.322, -0.552, -0.243, 0.154, -0.209, -0.211, -0.114, -0.105, -0.143, -0.206, 0.310, 0.378, -0.562, -0.123, 0.100, -0.112, -0.324, -0.125, 0.191, -0.165, -0.022, -0.115, -0.012, -0.181, -0.011, 0.085, 0.099, 0.119, 0.152, 0.161, 0.137, 0.136, 0.137, 0.010, 0.042, 0.040, 0.020, 0.014, 0.115, 0.074, 0.117, 0.104, 0.160, 0.131, 0.166, -0.095, 0.380, 0.360, 0.0, 0.0, 0.0, 0.281, 0.375]

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
if args.type != 'BR' and args.type != 'CF3' and args.type != 'CL' and args.type != 'CL2' and args.type != 'CH3' and args.type != 'NH2' and args.type != 'CLF' and args.type != 'H' and args.type != 'F':
        print('Error: Type must be either CH3, CF3, NH2, CL, CLF, F, or CL2')
        sys.exit()

#CHECK IF WE HAVE ALL REQUIRED FILES
for i in required_files:
         if not os.path.isfile(i):
                print('Error: ' + i + ' does not exist')
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
        print('Error: ' + phrase + ' does not exist in ' + file_name)
def set_charges_init(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        append_line(file_name, line_num, '    ab_crg 4164 0.078 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4165 -0.349 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4166 0.324 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4167 -0.448 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4168 -0.283 0.0\n')        
        append_line(file_name, line_num, '    ab_crg 4169 -0.109 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4170 -0.231 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4188 0.179 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4189 0.156 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4190 0.139 0.0\n') 
        append_line(file_name, line_num, '    ab_crg 4191 0.157 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4194 0.128 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4195 0.124 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4196 0.126 0.0\n')
        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] not in reg1_decharge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH3_charges[i]) + ' ' + str(CH3_charges[i]) + '\n')


def set_charges_vdw(file_name):
        line_num = get_line_number(file_name, 'reg1_res')
        append_line(file_name, line_num, '    ab_crg 4164 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4165 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4166 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4167 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4168 0.0 0.0\n')   
        append_line(file_name, line_num, '    ab_crg 4169 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4170 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4188 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4189 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4190 0.0 0.0\n')   
        append_line(file_name, line_num, '    ab_crg 4191 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4194 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4195 0.0 0.0\n')
        append_line(file_name, line_num, '    ab_crg 4196 0.0 0.0\n')
        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] not in reg1_decharge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH3_charges[i]) + ' ' + str(CH3_charges[i]) + '\n')


def recharge(file_name, reg1_atm_list):
        line_num = get_line_number(file_name, 'reg1_res')
        if args.type == 'CF3':
                charge_list = CF3_charges
        elif args.type == 'NH2':
                charge_list = NH2_charges
        elif args.type == 'CL':
                charge_list = CL_charges
        elif args.type == 'CL2':
                charge_list = CL2_charges
        elif args.type == 'CH3':
                charge_list = CH3_charges
        elif args.type == 'CLF':
                charge_list = CLF_charges
        elif args.type == 'H':
                charge_list = H_charges
        elif args.type == 'BR':
                charge_list = BR_charges
        elif args.type == 'F':
                charge_list = F_charges
        for i in range(len(reg1_atm_list)):
                if reg1_atm_list[i] in reg1_decharge_list:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' 0.0 ' + str(charge_list[i]) + '\n')
                else:
                        append_line(file_name, line_num, '    ab_crg ' + str(reg1_atm_list[i]) + ' ' + str(CH3_charges[i]) + ' ' + str(charge_list[i]) + '\n')

def set_vdw(file_name, group):
        line_num = get_line_number(file_name, 'reg1_res')
        if group == 'CF3':
                append_line(file_name, line_num, '    ab_vdw 4194 H1 F1\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 F1\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 F1\n')
        elif group == 'NH2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 H2\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 H2\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 N3\n')
        elif group == 'CL':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 CL\n')
        elif group == 'CL2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 H1 CL\n')
        elif group == 'H':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 H1\n')
        elif group == 'CLF':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 H1 F1\n')
        elif group == 'BR':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 BR\n')
        elif group == 'F':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 H1 DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 C4 F1\n')

def set_vdw_recharge(file_name, group):
        line_num = get_line_number(file_name, 'reg1_res')
        if group == 'CF3':
                append_line(file_name, line_num, '    ab_vdw 4194 F1 F1\n')
                append_line(file_name, line_num, '    ab_vdw 4195 F1 F1\n')
                append_line(file_name, line_num, '    ab_vdw 4196 F1 F1\n')
        elif group == 'NH2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 H2 H2\n')
                append_line(file_name, line_num, '    ab_vdw 4194 H2 H2\n')
                append_line(file_name, line_num, '    ab_vdw 4167 N3 N3\n')
        elif group == 'CL':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 CL CL\n')
        elif group == 'CL2':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 CL CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 CL CL\n')
        elif group == 'H':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 H1 H1\n')
        elif group == 'CLF':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 CL CL\n')
                append_line(file_name, line_num, '    ab_vdw 4191 F1 F1\n')
        elif group == 'BR':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 BR BR\n')
        elif group == 'F':
                append_line(file_name, line_num, '    ac_p_soft_vdw 0.5 4194 to 4196\n')
                append_line(file_name, line_num, '    ab_vdw 4194 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4195 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4196 DY DY\n')
                append_line(file_name, line_num, '    ab_vdw 4167 F1 F1\n')





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
print('============================ -CH3 to -' + args.type + ' =============================')
print('=======================================================================')
print('\n')
print('Number of Replicas: ' + replicas)
print('Number of Swaps: ' + swaps)
print('Number of Steps/Swaps: ' + steps)
print('Number of Steps (Serial Run): ' + str(args.serial) + ' Steps * ' + replicas + ' Replicas')
print('Lambda Decrement: ' + str(float(1.0/(num_tasks-1))))

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
                res_file_path = main_dir + '/CH3_decharge/output/2zf0_ac_start' + file_prefix + replicas
        else: 
                if len(replicas) == 1:
                        out_fol_prefix = '/CH3_decharge/output/acrun_00' 
                elif len(replicas) == 2:
                        out_fol_prefix = '/CH3_decharge/output/acrun_0' 
                elif len(replicas) == 3:
                        out_fol_prefix = '/CH3_decharge/output/acrun_' 

                res_file_path = main_dir + out_fol_prefix + replicas + file_prefix + replicas

        if os.path.isfile(res_file_path):
                print('RESTART FILE FROM DECHARGING STEP IS FOUND')
                print('DECHARGING STEP HAS ALREADY BEEN COMPLETED IN SOME OTHER PREVIOUS SIMULATIONS, NO NEED TO PERFORM HERE')
                print('PROCEEDING TO THE NEXT STEP')
        else:
                print('ERROR: RESTART FILE FROM DECHARGING STEP IS NOT FOUND, RUN DECHARGING STEP FIRST')
                sys.exit()
    
###############################vdW Step#################################
print('\n')
print('=======================================================================')
print('============================STARING VDW STEP===========================')
print('=======================================================================')
print('\n')

#Make vdW folder
if args.type == 'CF3':
        new_folder('CF3_vdW')
        vdw_folder_name = 'CF3_vdW'
elif args.type == 'NH2':
        new_folder('NH2_vdW')
        vdw_folder_name = 'NH2_vdW'     
elif args.type == 'CL':
        new_folder('CL_vdW')
        vdw_folder_name = 'CL_vdW'      
elif args.type == 'CL2':
        new_folder('CL2_vdW')
        vdw_folder_name = 'CL2_vdW'
elif args.type == 'H':
        new_folder('H_vdW')
        vdw_folder_name = 'H_vdW'
elif args.type == 'CLF':
        new_folder('CLF_vdW')
        vdw_folder_name = 'CLF_vdW'
elif args.type == 'BR':
        new_folder('BR_vdW')
        vdw_folder_name = 'BR_vdW'
elif args.type == 'F':
        new_folder('F_vdW')
        vdw_folder_name = 'F_vdW'


if args.type != 'CH3':

        #Get restart file from decharge output
        if args.swap == 0:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        else:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_00' + replicas + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_0' + replicas + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_' + replicas + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])

        #Update start, run, and check files in this directory
        set_vdw(start_file_name, args.type)
        set_vdw(run_file_name, args.type)
        set_vdw(check_file_name, args.type)
        set_charges_vdw(start_file_name)
        set_charges_vdw(check_file_name)
        set_charges_vdw(run_file_name)

        #UPDATE initial restart file in start file
        line_num = get_line_number(start_file_name, 'rest_in')
        replace_line(start_file_name, line_num, '    rest_in ' + starting_rest_in + '\n')

        #Run main_python_scripts_new
        subprocess.call(['python', main_script, replicas, swaps])
        #Process output from vdw run

        print('\n')
        print('Processing Output')

        time.sleep(1)
        os.chdir(main_dir)

###############################Recharging Step#################################
print('\n')
print('=======================================================================')
print('========================STARING RECHARGING STEP========================')
print('=======================================================================')
print('\n')


#Make recharge folder
if args.type == 'CF3':
        new_folder('CF3_recharge')
elif args.type == 'NH2':
        new_folder('NH2_recharge')      
elif args.type == 'CL':
        new_folder('CL_recharge')
elif args.type == 'CL2':
        new_folder('CL2_recharge')
elif args.type == 'CLF':
        new_folder('CLF_recharge')
elif args.type == 'BR':
        new_folder('BR_recharge')
elif args.type == 'F':
        new_folder('F_recharge')
elif args.type == 'H':
        new_folder('H_recharge')
elif args.type == 'CH3':
        new_folder('CH3_recharge')

        #Get restart file from decharge output for CH3 (no vdW step)
        if args.swap == 0:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/2zf0_ac_start' + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])
        else:
                if len(replicas) == 1:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_00' + replicas + '/ac.res00' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res00' + replicas, starting_rest_in])
                elif len(replicas) == 2:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_0' + replicas + '/ac.res0' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res0' + replicas, starting_rest_in])
                elif len(replicas) == 3:
                        subprocess.call(['cp', main_dir + '/CH3_decharge/output/acrun_' + replicas + '/ac.res' + replicas, '.'])
                        subprocess.call(['mv', 'ac.res' + replicas, starting_rest_in])

if args.type != 'CH3':

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

#Update start, run, and check files in this directory
set_vdw_recharge(start_file_name, args.type)
set_vdw_recharge(run_file_name, args.type)
set_vdw_recharge(check_file_name, args.type)
recharge(start_file_name, reg1_atm_list)
recharge(check_file_name, reg1_atm_list)
recharge(run_file_name, reg1_atm_list)

#Run main_script_v1.py
subprocess.call(['python', main_script, replicas, swaps])

#Process output from recharging run
print('\n')
print('Processing Output')

time.sleep(1)

print('All Done')


