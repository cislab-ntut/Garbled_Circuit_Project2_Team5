import sys

input_circuit = input("please input the circuit: ")
op_table = ['or', 'and', 'xor', 'nand', 'nor']
lst = input_circuit.split(' ')
circuit = dict()
operator = list()
input = list()
input_table = dict()
count = 1
for i in lst:
	if i == "(":
		continue
	elif i == ")":
		index = len(circuit)
		circuit[index] = dict()
		circuit[index]['op'] = operator.pop()
		circuit[index]['input1'] = input.pop()
		circuit[index]['input2'] = input.pop()
		circuit[index]['output'] = count
		input.append(count)
		count += 1
	elif i in op_table:
		operator.append(i)
	else:
		input.append(count)
		input_table[i] = count
		count += 1
for i in circuit:
	print(circuit[i])

print(input_table)