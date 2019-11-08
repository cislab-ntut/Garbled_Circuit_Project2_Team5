import sys
import gate
import random
import enigma_func as enigma

def exist(value):
	global random_table
	if value in random_table:
		return True
	else:
		return False
def get_random():
	global random_table
	val = random.randint(0, 25)
	while exist(val):
		val = random.randint(0, 25)
	random_table.append(val)
	return val

def get_out_org(input1_index, input2_index, t_table):
	lst = list()
	for i in range(len(t_table[0])):
		if input1_index == t_table[0][i]:
			lst.append(i)
	for j in lst:
		if input2_index == t_table[1][j]:
			return t_table[2][j]

random_table = list()
NANDList = list()
ANDList = list()
NORList = list()
ORList = list()
XORList = list()


for i in range(2):
	for j in range(2):
		a = gate.Gate(i,j,'AND')
		ANDList.append(a.call())
		b = gate.Gate(i,j,'OR')
		ORList.append(b.call())
		c = gate.Gate(i,j,'XOR')
		XORList.append(c.call())
		d = gate.Gate(i,j,'NAND')
		NANDList.append(d.call())
		e = gate.Gate(i,j,'NOR')
		NORList.append(e.call())

a = [0,0,1,1]
b = [0,1,0,1]
nimplyList = [0,0,1,0]
gate_table = {	'and':[a,b,ANDList],
				'or':[a,b,ORList],
				'xor':[a,b,XORList],
				'nand':[a,b,NANDList],
				'nor':[a,b,NORList],
				'nimply':[a,b,nimplyList]	}
print(gate_table['xor'])

input_circuit = input("please input the circuit: ")
op_table = ['or', 'and', 'xor', 'nand', 'nor']

lst = input_circuit.split(' ')
circuit = dict()
operator = list()
inp = list()
truth_table = dict()

enc_table = dict()
enc_t_table = dict()
enc_to_org = dict()
input_to_enc = dict()

input_table = dict()
input_table_num = list()
count = 1
for i in lst:
	if i == "(":
		continue
	elif i == ")":
		index = len(circuit)
		circuit[index] = dict()
		truth_table[index] = dict()
		op = operator.pop()
		circuit[index]['input2'] = inp.pop()
		circuit[index]['input1'] = inp.pop()
		circuit[index]['output'] = count
		truth_table[index]['truth_table'] = gate_table[op]
		inp.append(count)
		count += 1
	elif i in op_table:
		operator.append(i)
	else:
		inp.append(count)
		input_table[i] = count
		input_table_num.append(count)
		count += 1
print(circuit)
label = dict()
for i in range(1, inp[0]+1,1):
	label[i] = [get_random(), get_random()]
	input_to_enc[i] = dict()
	input_to_enc[i][0] = label[i][0]
	input_to_enc[i][1] = label[i][1]
	enc_to_org[label[i][0]] = 0
	enc_to_org[label[i][1]] = 1
#print(input_to_enc)

for index in range(0, len(circuit), 1):
	g = circuit[index]
	input1 = label[g['input1']]
	input2 = label[g['input2']]
	output = label[g['output']]
	#print(input1, input2, output)
	
	org_truth_table = truth_table[index]['truth_table']
	#print(org_truth_table)
	enc_t_table[index] = dict()
	lst = list()
	ans = list()
	for i in input1:
		for j in input2:

			out_org = get_out_org(enc_to_org[i], enc_to_org[j], org_truth_table)
			#print(g['output'], out_org)
			out_val = input_to_enc[g['output']][out_org]
			t2 = (i, j)
			lst.append([enigma.enigma([i, j, 0], out_val), hash((i, j, out_val))])
			ans.append([enigma.enigma([i, j, 0], lst[len(lst)-1][0]), out_val, out_org])
			#lst.append(enc_t_table[index][t2])
			#enc_to_org[enc_t_table[index][t2]] = org_truth_table[2][out_org]
	enc_table[g['output']] = lst
	#print(lst)
	#print(ans)


'''
for index in range(0,len(circuit),1):
	g = circuit[index]
	#print(g)
	input1 = g['input1']
	input2 = g['input2']
	output = g['output']
	org_truth_table = truth_table[index]['truth_table']
	if input1 in enc_table:
		input1 = enc_table[input1]
	else:
		input_to_enc[input1] = dict()
		ID = input1
		input1 = [get_random(), get_random()]
		input_to_enc[ID][0] = input1[0]
		input_to_enc[ID][1] = input1[1]
		enc_to_org[input1[0]] = 0
		enc_to_org[input1[1]] = 1
	if input2 in enc_table:
		input2 = enc_table[input2]
	else:
		input_to_enc[input2] = dict()
		ID = input2
		input2 = [get_random(), get_random()]
		input_to_enc[ID][0] = input2[0]
		input_to_enc[ID][1] = input2[1]
		enc_to_org[input2[0]] = 0
		enc_to_org[input2[1]] = 1

	enc_t_table[index] = dict()
	lst = list()
	for i in input1:
		for j in input2:

			out_org = get_out_org(enc_to_org[i], enc_to_org[j], org_truth_table)
			t2 = (i, j)
			enc_t_table[index][t2] = get_random()
			lst.append(enc_t_table[index][t2])
			enc_to_org[enc_t_table[index][t2]] = org_truth_table[2][out_org]
	enc_table[output] = lst
'''
print("input_to_enc", input_to_enc)
print("enc_to_org", enc_to_org)
c_index = 0
input_value = input("input enter value (0 or 1): ")
value_list = dict()
input_value = input_value.split(' ')
input_value = [int(x) for x in input_value]
for index in range(len(circuit)):
	g = circuit[index]
	input1 = g['input1']
	input2 = g['input2']
	output = g['output']
	if input1 in input_table_num:

		value_list[input1] = input_to_enc[input1][input_value[c_index]]
		c_index += 1
	if input2 in input_table_num:
		value_list[input2] = input_to_enc[input2][input_value[c_index]]
		c_index += 1
	if c_index == len(input_value):
		break
#print(value_list)
for index in range(len(circuit)):
	g = circuit[index]
	index1 = value_list[g['input1']]
	index2 = value_list[g['input2']]
	for i in enc_table[g['output']]:
		dec = enigma.enigma([index1, index2, 0], i[0])
		if hash((index1, index2, dec)) == i[1]:
			print(dec)
			value_list[g['output']] = dec
			break

print(enc_to_org)
print(value_list)
print(enc_to_org[value_list[len(value_list)]])

'''
for index in range(len(circuit)):
	g = circuit[index]
	index1 = g['input1']
	index2 = g['input2']
	value_list[g['output']] = enc_t_table[index][(value_list[index1], value_list[index2])]
#print(enc_to_org)
print(enc_t_table)
#print(value_list)
#print(len(value_list))
print(enc_to_org[value_list[len(value_list)]])
'''
'''
print("encoding to org:")
print(enc_to_org)
print("-------------------------------------------")
for i in enc_t_table:
	print(enc_t_table[i])
'''
'''
for i in circuit:
	print(circuit[i])

print(input_table)
'''