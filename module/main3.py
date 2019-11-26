import create_circuit3 as cc
import sys
'''
3-bit	0.3min
4-bit	2min
5-bit	12min
6-bit	72min
7-bit	7.2hr
8*bit	43.2hr
'''
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

def addition(sum_table, s_table, a, b):
	length = len(sum_table)
	#print(sum_table)
	
	new_sum = list()
	if len(b) < length:
		for i in range(length - len(b)):
			b.append(0)
	if len(a) < length:
		for i in range(length - len(a)):
			a.append(0)
	
	s = 0

	for i in range(length):
		print([a[i],b[i],s])
		enc_sum_value = cc.enc_input([a[i],b[i],s],sum_table[i]["circuit"],sum_table[i]["input_to_enc"], sum_table[i]["input_table_num"])
		new_sum.append(cc.dec(enc_sum_value, sum_table[i]["circuit"], sum_table[i]["enc_table"], sum_table[i]["enc_to_org"]))
		enc_s_value = cc.enc_input([a[i],b[i],a[i],b[i],s],s_table[i]["circuit"],s_table[i]["input_to_enc"], s_table[i]["input_table_num"])
		s = cc.dec(enc_s_value, s_table[i]["circuit"], s_table[i]["enc_table"], s_table[i]["enc_to_org"])
		print("s:",s)
	'''
	if s == 1:
		new_sum.append(s)
	'''
	while True:
		if len(new_sum) == 1:
			break
		if new_sum[len(new_sum)-1] == 0:
			new_sum.pop()
		else:
			break
	return new_sum
	

def subtraction(d_table, s_table, a,b):
	length = len(d_table)
	diff = list()
	if len(b) < length:
		for i in range(length - len(b)):
			b.append(0)
	if len(a) < length:
		for i in range(length - len(a)):
			a.append(0)
	s = 0
	for i in range(length):
		enc_diff_value = cc.enc_input([a[i],b[i],s],d_table[i]["circuit"],d_table[i]["input_to_enc"], d_table[i]["input_table_num"])
		diff.append(cc.dec(enc_diff_value, d_table[i]["circuit"], d_table[i]["enc_table"], d_table[i]["enc_to_org"]))
		enc_s_value = cc.enc_input([b[i],s,b[i],s,a[i]],s_table[i]["circuit"],s_table[i]["input_to_enc"], s_table[i]["input_table_num"])
		s = cc.dec(enc_s_value, s_table[i]["circuit"], s_table[i]["enc_table"], s_table[i]["enc_to_org"])

	while True:
		if len(diff) == 1:
			break
		if diff[len(diff)-1] == 0:
			diff.pop()
		else:
			break
	return diff
'''
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
'''
def create_circuit(size, max_val,func):
	garbled_circuit = list()
	for i in range(max_val):
		garbled_circuit.append(list())
		for j in range(size):
			circuit, input_to_enc, enc_table, enc_to_org, input_table_num = cc.create_garbled_circuit(func)
			d = {"circuit":circuit,"input_to_enc":input_to_enc,"enc_table":enc_table,"enc_to_org":enc_to_org, "input_table_num":input_table_num}
			garbled_circuit[i].append(d)
	return garbled_circuit

how_many_bit = 4#8
p = 13#65533
max_val = list()
for i in range(how_many_bit):
	max_val.append(1)
#print(max_val)
max_val = bin_to_dec(max_val)
sub_level = pow(max_val, 2) // p
#print(sub_level)
add_sum = list()
add_s = list()
sub_diff = list()
sub_s = list()
comp = list()
equal = list()
print("create circuit!")
for i in range(max_val-1):
	size = 2*how_many_bit
	add_sum.append(create_circuit(size, max_val, circuit_table["add_sum"]))
	#print(add_sum)
	add_s.append(create_circuit(size, max_val, circuit_table["add_s"]))
#print(len(add_sum),len(add_sum[0]))
#print(type(add_sum))
size = 2*how_many_bit
for i in range(max_val-1):
	sub_diff.append(create_circuit(size, sub_level, circuit_table["sub_diff"]))
	#print(sub_diff)
	sub_s.append(create_circuit(size, sub_level, circuit_table["sub_s"]))
	#comp.append(create_circuit(size, max_val, circuit_table["comp_val"]))
	#equal.append(create_circuit(size, max_val, circuit_table["equal"]))
#print(len(sub_diff),len(sub_diff[0]))
print("success!")
f = open(str(how_many_bit)+"bit.txt","w")
f.write(str(add_sum))
f.close()
#g = int(input("please enter g: "))
#x = int(input("please enter x: "))
g = 15#65535
x = 15#65535
#p = int(input("please enter p: "))
g_bin = dec_to_bin(g)
p = dec_to_bin(p)

g_square = g_bin
output = [0]

for i in range(max_val-1):
	sub = p
	if i >= x-1:
		output = g_square
		g_square = [0]
	for j in range(len(add_sum[i])):
		if j == g:
			g_square = [0]
		output = addition(add_sum[i][j], add_s[i][j], output, g_square)
	#print("after add",bin_to_dec(output))
	for j in range(len(sub_diff[i])):
		if bin_to_dec(output) < bin_to_dec(p):
			sub = [0]
		output = subtraction(sub_diff[i][j], sub_s[i][j], output, sub)
	#print("after sub",bin_to_dec(output))
	g_square = output
	if i != max_val-2:
		output = [0]
print(bin_to_dec(output))