import create_circuit2 as cc
import sys

#p = 2^255 - 19 = 57896044618658097711785492504343953926634992332820282019728792003956564819949
circuit_table = {	"add_sum" : "( ( A xor B ) xor S )",
					"add_s" : "( ( A and B ) or ( ( A or B ) and C ) )",
					"sub_diff" : "( ( A xor B ) xor S )",
					"sub_s" : "( ( B and C ) or ( ( B or C ) nimply A ) )",
					"comp_val" : "( A nimply B )",
					"equal" : "( A xor B )"}

def dec_to_bin(dec):
	lst = list()
	while dec > 0:
		lst.append(dec%2)
		dec = dec // 2
	return lst

def bin_to_dec(binary_num):
	count = 1
	output = 0
	for i in binary_num:
		output += i * count
		count = count * 2
	return output

def addition(a, b):

	new_sum = list()
	if len(b) < len(a):
		for i in range(len(a) - len(b)):
			b.append(0)
	if len(a) < len(b):
		for i in range(len(b) - len(a)):
			a.append(0)
	s = 0
	for i in range(len(a)):
		new_sum.append(cc.garbled_circuit(circuit_table["add_sum"],[a[i],b[i],s]))
		s = cc.garbled_circuit(circuit_table["add_s"], [a[i],b[i], a[i], b[i],s])
	if s == 1:
		new_sum.append(s)
	return new_sum

def subtraction(a,b):
	diff = list()
	if len(b) < len(a):
		for i in range(len(a) - len(b)):
			b.append(0)
	if len(a) < len(b):
		for i in range(len(b) - len(a)):
			a.append(0)
	s = 0
	for i in range(len(a)):
		diff.append(cc.garbled_circuit(circuit_table["sub_diff"],[a[i],b[i],s]))
		s = cc.garbled_circuit(circuit_table["sub_s"], [b[i],s, b[i], s,a[i]])
	while diff[len(diff)-1] == 0 and len(diff) > 1:
		diff.pop()
	return diff

def less(a,b):
	if len(b) < len(a):
		for i in range(len(a) - len(b)):
			b.append(0)
	if len(a) < len(b):
		for i in range(len(b) - len(a)):
			a.append(0)
	for i in range(len(a)-1, -1, -1):
		comp_val = cc.garbled_circuit(circuit_table["comp_val"],[a[i],b[i]])
		equal = cc.garbled_circuit(circuit_table["equal"],[a[i],b[i]])
		if comp_val == 1:
			return False
		elif comp_val == 0 and equal == 0:
			continue
		elif comp_val == 0 and equal == 1:
			return True
	return True

g = int(input("please enter g: "))
x = int(input("please enter x: "))
p = int(input("please enter p: "))
g_bin = dec_to_bin(g)
p = dec_to_bin(p)
iteration = pow(g,x-1)
#print(iteration)
#print(type(iteration))
#print(addition([1], g_bin))
#print(subtraction(g_bin,[1]))
#print(less(p, g_bin))
g_square = g_bin
output = g_bin
for i in range(x-1):
	for i in range(g-1):
		output = addition(output, g_square)
	g_square = output
while less(p, output) == True:
	output = subtraction(output, p)
print(bin_to_dec(output))
'''
for i in range(iteration):
	output = addition(output, g_bin)
	if less(p, output) == True:
		output = subtraction(output, p)
print(output)
print(bin_to_dec(output))
'''
#print(bin_to_dec(dec_to_bin(int(sys.argv[1]))))
#print(cc.garbled_circuit(circuit_table['add_s'], [1,0,1,0,0]))