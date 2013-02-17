import os
import sys
import re

variable_address_start = 16
variable_address_counter = 0

variable_symbol_table = {
"SP" : 0,
"LCL" : 1,
"ARG" : 2,
"THIS" : 3,
"THAT" : 4,
"R0" : 0,
"R1" : 1,
"R2" : 2,
"R3" : 3,
"R4" : 4,
"R5" : 5,
"R6" : 6,
"R7" : 7,
"R8" : 8,
"R9" : 9,
"R10" : 10,
"R11" : 11,
"R12" : 12,
"R13" : 13,
"R14" : 14,
"R15" : 15,
"SCREEN" : 16384,
"KBD" : 24576

      }
rom_symbol_table = {        }

rom_counter = 0
ram_symbol_pattern = "([_.:$A-z][_.:$A-z0-9]*)"
rom_symbol_pattern = "\(([_.:$A-z][_.:$A-z0-9]*)\)"

comp_table = {

"0" : "0101010",
"1" : "0111111",
"-1" : "0111010",
"D" : "0001100",
"A" : "0110000",
"!D" : "0001101",
"!A" : "0110001",
"-D" : "0001111",
"-A" : "0110001",
"D+1" : "0011111",
"A+1" : "0110111",
"D-1" : "0001110",
"A-1" : "0110010",
"D+A" : "0000010",
"D-A" : "0010011",
"A-D" : "0000111",
"D&A" : "0000000",
"D|A" : "0010101",
"M" : "1110000",
"!M" : "1110001",
"-M" : "1110011",
"M+1" : "1110111",
"D+M" : "1000010",
"D-M" : "1010011",
"M-D" : "1000111",
"D&M" : "1000000",
"D|M" : "1010101",
"M-1" : "1110010",


}





file_line_number = 0


input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0]+".hack"

output = open(output_file,"w")

lines = open(input_file).readlines()

def getBin(x):
	out = str(bin(int(x)))[2:]
	out = "0"*(15-len(out))+out
	if len(out) != 15:
		print "ERRRRR"
		print x
		print out
		exit()
	return out
def emit(line):
	output.write(line+"\n")	
	

for line in lines:
	file_line_number = file_line_number+1
	if len(line.strip()) == 0: continue
	if re.match("//.*",line.strip()) : continue
	match = re.match(rom_symbol_pattern,line.strip())
	if match != None:
		if not match.group(1) in rom_symbol_table:
			rom_symbol_table[match.group(1)] = rom_counter
			continue
		else:
			raise Exception("Duplicate ROM Symbol at line "+str(file_line_number))
	rom_counter = rom_counter+1

file_line_number = 0
for linee in lines:
	line = linee.strip()
	file_line_number = file_line_number+1
	if len(line.strip()) == 0: continue
	if re.match("//.*",line.strip()) : continue
        if re.match(rom_symbol_pattern,line.strip()): continue
	
	if re.match("@.*",line.strip()):
		match = re.match("@([0-9]+)",line.strip())
		if match:
			emit("0"+getBin(match.group(1)))
			continue			
		match = re.match("@"+ram_symbol_pattern,line.strip())
		if match and not match.group(1) in variable_symbol_table and not match.group(1) in rom_symbol_table:
			variable_symbol_table[match.group(1)] = variable_address_start + variable_address_counter
			variable_address_counter = variable_address_counter+1	
		if match.group(1) in variable_symbol_table:
			emit("0"+getBin(variable_symbol_table[match.group(1)]))
		else:
			emit("0"+getBin(rom_symbol_table[match.group(1)]))
	else:
		dst = [0,0,0]
		if "=" in line:
			dest_str = line.split("=")[0]
			if "M" in dest_str:
				dst[2] = 1
			if "D" in dest_str:
				dst[1] = 1
			if "A" in dest_str:
				dst[0] = 1
		jmp = [0,0,0]
		if ";" in line:
			jump_str = line.split(";")[1]
			if jump_str == "JGT":
				jmp = [0,0,1]	
			if jump_str == "JEQ":
				jmp = [0,1,0]	
			if jump_str == "JGE":
				jmp = [0,1,1]	
			if jump_str == "JLT":
				jmp = [1,0,0]	
			if jump_str == "JNE":
				jmp = [1,0,1]	
			if jump_str == "JLE":
				jmp = [1,1,0]	
			if jump_str == "JMP":
				jmp = [1,1,1]	
		comp_str = line.split("=").pop().split(";")[0]
		comp = comp_table[comp_str]
		

		binary = "111"+comp+"".join(map(str,dst))+"".join(map(str,jmp))
		if len(binary) != 16:
			print line
			print comp
			print dst
			print jmp
			print binary
			print len(binary)
			exit() 
		emit(binary )

output.close()



