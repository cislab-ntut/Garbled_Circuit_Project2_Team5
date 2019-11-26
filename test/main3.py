import create_circuit3 as cc
import sys
import json
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
	#print("length:",length)
	
	new_sum = list()
	if len(b) < length:
		for i in range(length - len(b)):
			b.append(0)
	if len(a) < length:
		for i in range(length - len(a)):
			a.append(0)

	s = 0
	for i in range(length):
		#print([a[i],b[i],s])
		enc_sum_value = cc.enc_input([a[i],b[i],s],sum_table[str(i)]["circuit"],sum_table[str(i)]["input_to_enc"], sum_table[str(i)]["input_table_num"])
		new_sum.append(cc.dec(enc_sum_value, sum_table[str(i)]["circuit"], sum_table[str(i)]["enc_table"], sum_table[str(i)]["enc_to_org"]))
		enc_s_value = cc.enc_input([a[i],b[i],a[i],b[i],s],s_table[str(i)]["circuit"],s_table[str(i)]["input_to_enc"], s_table[str(i)]["input_table_num"])
		s = cc.dec(enc_s_value, s_table[str(i)]["circuit"], s_table[str(i)]["enc_table"], s_table[str(i)]["enc_to_org"])
		#print("new_sum:",bin_to_dec(new_sum))
		#print("s:",s)
		#print("enc_s_value",enc_s_value)
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
	#print("new sum:",new_sum)
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
		enc_diff_value = cc.enc_input([a[i],b[i],s],d_table[str(i)]["circuit"],d_table[str(i)]["input_to_enc"], d_table[str(i)]["input_table_num"])
		diff.append(cc.dec(enc_diff_value, d_table[str(i)]["circuit"], d_table[str(i)]["enc_table"], d_table[str(i)]["enc_to_org"]))
		enc_s_value = cc.enc_input([b[i],s,b[i],s,a[i]],s_table[str(i)]["circuit"],s_table[str(i)]["input_to_enc"], s_table[str(i)]["input_table_num"])
		s = cc.dec(enc_s_value, s_table[str(i)]["circuit"], s_table[str(i)]["enc_table"], s_table[str(i)]["enc_to_org"])

	while True:
		if len(diff) == 1:
			break
		if diff[len(diff)-1] == 0:
			diff.pop()
		else:
			break
	return diff

def create_circuit(size, max_val,func):
	garbled_circuit = dict()
	for i in range(max_val):
		garbled_circuit[str(i)] = dict()
		for j in range(size):
			circuit, input_to_enc, enc_table, enc_to_org, input_table_num = cc.create_garbled_circuit(func)
			d = {"circuit":circuit,"input_to_enc":input_to_enc,"enc_table":enc_table,"enc_to_org":enc_to_org, "input_table_num":input_table_num}
			garbled_circuit[str(i)][str(j)] = d
	#print(garbled_circuit)
	return garbled_circuit

how_many_bit = 9#8
p = 509#65533
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
savepath = "circuit/"
outname = ["add_sum", "add_s", "sub_diff", "sub_s"]
print("create circuit!")

for i in range(max_val-1):
	size = 2*how_many_bit
	add_sum = create_circuit(size, max_val, circuit_table["add_sum"])
	with open(savepath+outname[0]+str(i)+".json","w") as f:
		json.dump(add_sum, f)
	f.close()
	#print(add_sum)
	add_s = create_circuit(size, max_val, circuit_table["add_s"])
	with open(savepath+outname[1]+str(i)+".json","w") as f1:
		json.dump(add_s, f1)
	f1.close()
#print(len(add_sum),len(add_sum[0]))

size = 2*how_many_bit
for i in range(max_val-1):
	sub_diff = create_circuit(size, sub_level, circuit_table["sub_diff"])
	#print(sub_diff)
	with open(savepath+outname[2]+str(i)+".json","w") as f2:
		json.dump(sub_diff, f2)
	f2.close()
	sub_s = create_circuit(size, sub_level, circuit_table["sub_s"])
	with open(savepath+outname[3]+str(i)+".json","w") as f3:
		json.dump(sub_s, f3)
	f3.close()
	#comp.append(create_circuit(size, max_val, circuit_table["comp_val"]))
	#equal.append(create_circuit(size, max_val, circuit_table["equal"]))
#print(len(sub_diff),len(sub_diff[0]))
print("success!")

#g = int(input("please enter g: "))
#x = int(input("please enter x: "))
g = 511#65535
x = 511#65535
#p = int(input("please enter p: "))
g_bin = dec_to_bin(g)
p = dec_to_bin(p)

g_square = g_bin
output = [0]
add_sum = dict()
add_s = dict()
sub_diff = dict()
sub_s = dict()
for i in range(max_val-1):
	#print("i:",i)
	sub = p
	if i >= x-1:
		output = g_square
		g_square = [0]
	with open(savepath+outname[0]+str(i)+".json","r") as f:
		add_sum = json.load(fp=f)
	with open(savepath+outname[1]+str(i)+".json","r") as f1:
		add_s = json.load(fp=f1)
	with open(savepath+outname[2]+str(i)+".json","r") as f2:
		sub_diff = json.load(fp=f2)
	with open(savepath+outname[3]+str(i)+".json","r") as f3:
		sub_s = json.load(fp=f3)
	f.close()
	f1.close()
	f2.close()
	f3.close()
	#print("len add sum")
	#print(add_sum)
	#print("g_square")
	#print(bin_to_dec(g_square))
	#print(bin_to_dec(output))
	for j in range(len(add_sum)):
		if j == g:
			g_square = [0]
		#print("g_square",g_square)
		#print(add_sum[str(j)])
		output = addition(add_sum[str(j)], add_s[str(j)], output, g_square)
		#print("output:",bin_to_dec(output))
	#print("after add",bin_to_dec(output))
	for j in range(len(sub_diff)):
		if bin_to_dec(output) < bin_to_dec(p):
			sub = [0]
		output = subtraction(sub_diff[str(j)], sub_s[str(j)], output, sub)
	#print("after sub",bin_to_dec(output))
	g_square = output
	if i != max_val-2:
		output = [0]
print(bin_to_dec(output))