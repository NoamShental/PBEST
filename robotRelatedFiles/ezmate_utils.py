from scipy import io
import pandas as pd
import numpy as np
import sys 
import scipy
import scipy.stats
import glob
from sklearn import metrics
import seaborn as sns
import getpass
import os
import re       # regular expressions
from itertools import chain


def generate_LT_command(source_plate, destination_plate, source_well, destination_well, source_volume, transfer_volume, aspirate_speed=(2, 5),
                    dispense_speed=(3, 5), air_gap=5, tip=(1, 1, 0), mix=(2, 3, 70, 4), reverse=5):
	"""
	Generate a single Liquid Transfer command in the EZMate format

	Parameters:
	----------

	source_plate: ['A' |'B' | 'C' | 'D' | 'E' | 'R1' | 'R2']
	    name of source location on the robot dispenser bed. A-E are plates and R1 and R2 are reservoires.
	destination_plate: ['A' |'B' | 'C' | 'D' | 'E' | 'R1' | 'R2']
	    name of destination plate on robot dispenser. A-E are plates and R1 and R2 are reservoires
	source_well: [ tuple (<str>, <int>) | int]
		location of source well on source plate. If plate is a tuple (row, column) if reservoir is an integer [1-3]
	destination_well: [tuple | int]
		location of destination well on source plate. If plate is a tuple (row, column) if reservoir is an integer [1-3]
	source_volume: int
		amount of volume in source well
	volume: int 
		dispense volume
	aspirate_speed: (int, int)
		(<depth>, <speed>), where depth - 1: under liquid level, 2: well bottom, and speed - [1-5]
	dispense_speed: (int, int)
		(<depth>, <speed>), where depth - 1: under liquid, 2: well bottom, 3: well top
	air_gap: int
		air gap volume, default set to 5.
	tip: (int, int, int)
		(<tip_change>, <tip_change_frequency>, <command_count>), where tip_change - 0: disable, 1: enable, 
		tip_change_frequency - 1: before each aspiration, 2: when a command finishes, 3: afer command_count commands, and 
		command_count: number of commands if tip_change_frequency is set to 3.
	mix: (int, int, int, int)
		(<when>. <times>, <rate>, <speed>) where, when - 1: after dispense, 2: before aspiration, 3: both dispense and aspiration, 
		times: number of times to mix, rate - amount to mix from 40-70% and speed - mix speed 1-5.
	reverse: int
		enable reverse pipetting function. int defines volume
	blow_out: int
		role unclear....
	"""                   
	command_str = 'LT,' + str(transfer_volume) + '\n'
	command_str += 'AspirateSpeed,' + str(aspirate_speed[0]) + ',' + str(aspirate_speed[1]) + '\n'
	command_str += 'DispenseSpeed,' + str(dispense_speed[0]) + ',' + str(dispense_speed[1]) + '\n'
	command_str += 'AIRGAP,' + str(air_gap) + '\n'
	command_str += 'TIP,' + str(tip[0]) + ',' + str(tip[1]) + ',' + str(tip[2]) + '\n'
	command_str += 'MIX,' + str(mix[0]) + ',' + str(mix[1]) + ',' + str(mix[2]) + ',' + str(mix[3]) + '\n'
	command_str += 'REVERSE,' + str(reverse) + '\n'
	command_str += 'Source,' + source_plate + ',' + source_well[0] + '-' + str(source_well[1]) + \
					',Source,Source,' + str(source_volume) + '\n'
	command_str += 'Destination,' + destination_plate + ',' + destination_well[0] + '-' + str(destination_well[1]) + \
					',Destination,Destination \n'
	command_str += 'LT'

	return command_str


def generate_MD_command(source_plate, destination_plates, source_well, destination_wells, source_volume, transfer_volume, aspirate_speed=(2, 5),
                    dispense_speed=(3, 5), air_gap=5, tip=(1, 1, 0), mix=(2, 3, 70, 4), reverse=5):
	"""
	Generate a multi-dispense Liquid Transfer command in the EZMate format

	Parameters:
	----------

	source_plate: ['A' |'B' | 'C' | 'D' | 'E' | 'R1' | 'R2']
	    name of source location on the robot dispenser bed. A-E are plates and R1 and R2 are reservoires.
	destination_plates: list
	    name of destination plates on robot dispenser. values can be ['A' |'B' | 'C' | 'D' | 'E' | 'R1' | 'R2']
		A-E are plates and R1 and R2 are reservoires
	source_well: [ tuple (<str>, <int>) | int]
		location of source well on source plate. If plate is a tuple (row, column) if reservoir is an integer [1-3]
	destination_wells: list of [tuple | int]
		list of locations of destination wells on source plate. Each entry is a tuple or an int. 
		If plate is a tuple (row, column) if reservoir is an integer [1-3]
	source_volume: int
		amount of volume in source well
	volume: int 
		dispense volume
	aspirate_speed: (int, int)
		(<depth>, <speed>), where depth - 1: under liquid level, 2: well bottom, and speed - [1-5]
	dispense_speed: (int, int)
		(<depth>, <speed>), where depth - 1: under liquid, 2: well bottom, 3: well top
	air_gap: int
		air gap volume, default set to 5.
	tip: (int, int, int)
		(<tip_change>, <tip_change_frequency>, <command_count>), where tip_change - 0: disable, 1: enable, 
		tip_change_frequency - 1: before each aspiration, 2: when a command finishes, 3: afer command_count commands, and 
		command_count: number of commands if tip_change_frequency is set to 3.
	mix: (int, int, int, int)
		(<when>. <times>, <rate>, <speed>) where, when - 1: after dispense, 2: before aspiration, 3: both dispense and aspiration, 
		times: number of times to mix, rate - amount to mix from 40-70% and speed - mix speed 1-5.
	reverse: int
		enable reverse pipetting function. int defines volume
	blow_out: int
		role unclear....
	"""                   
	command_str = 'MD,' + str(transfer_volume) + '\n'
	command_str += 'AspirateSpeed,' + str(aspirate_speed[0]) + ',' + str(aspirate_speed[1]) + '\n'
	command_str += 'DispenseSpeed,' + str(dispense_speed[0]) + ',' + str(dispense_speed[1]) + '\n'
	command_str += 'AIRGAP,' + str(air_gap) + '\n'
	command_str += 'TIP,' + str(tip[0]) + ',' + str(tip[1]) + ',' + str(tip[2]) + '\n'
	command_str += 'MIX,' + str(mix[0]) + ',' + str(mix[1]) + ',' + str(mix[2]) + ',' + str(mix[3]) + '\n'
	command_str += 'REVERSE,' + str(reverse) + '\n'
	command_str += 'Source,' + source_plate + ',' + source_well[0] + '-' + str(source_well[1]) + \
					',Source,Source,' + str(source_volume) + '\n'
	for p, d in zip(destination_plates, destination_wells):

		command_str += 'Destination,' + p + ',' + d[0] + '-' + str(d[1]) + \
						',Destination,Destination \n'
	command_str += 'MD\n'

	return command_str


def sample_list_to_plate_map(sample_list, plate_num, plate_format='96_well'):
	"""
	Generate plate map from samples for different plate formats. Assumes sample_list is shorter or equal in size to the current plate size:

	"""
	if plate_format == '96_well':
		columns = np.arange(1,13)
		index = pd.Index(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
	elif plate_format == '48_well':
		columns = np.arange(1,9)
		index = pd.Index(['A', 'B', 'C', 'D', 'E', 'F'])


	plate_df = pd.DataFrame(columns=columns, index=index)
	sample_df = pd.DataFrame(index=sample_list, columns=['Plate', 'Row', 'Column'])

	# generate sample_df - each sample lists its row and column location on plate. Only sets this for samples that exist
	for i, n in enumerate(index):
		for j, m in enumerate(columns):
			#print(np.ravel_multi_index(multi_index=(i, j), dims=(len(index), len(columns))))
			curr_ind = np.ravel_multi_index(multi_index=(i, j), dims=(len(index), len(columns)))
			if curr_ind < len(sample_list):
				sample_df.iloc[curr_ind] = [plate_num, n, m]

	for s in sample_df.index:
		plate_df.loc[sample_df.loc[s].Row, sample_df.loc[s].Column] = s
	return plate_df, sample_df


