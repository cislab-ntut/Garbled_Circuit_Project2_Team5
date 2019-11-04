
alphet_to_num = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,
				"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25}
num_to_alphet = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",
				19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:"Z"}

def rotate(rotor):
	tmp_r = rotor.pop(0)
	rotor.append(tmp_r)
	return rotor
	
def initial(outerrotor,innerrotor , startposition):
	while(outerrotor[0] !=startposition):
		outerrotor = rotate(outerrotor)
		innerrotor = rotate(innerrotor)
	return outerrotor , innerrotor

def read_file(filename):
	global alphet_to_num
	f = open(filename, "r")
	lines = f.readlines()
	string = ""
	for line in lines:
		line.strip('\n')
		string = string+line
	lst = list(string)
	file = [alphet_to_num[char] for char in lst]
	return file

def enigma(start, input_value):
	global alphet_to_num, num_to_alphet
	
	plugboard = read_file('plugboard_my.txt')
	RIII_outside = read_file('outside.txt')
	RII_outside = read_file('outside.txt')
	RI_outside = read_file('outside.txt')
	rotorI = read_file('Rotor_I_web.txt')
	rotorII = read_file('Rotor_II_web.txt')
	rotorIII = read_file('Rotor_III_web.txt')
	reflector = read_file('reflector_web.txt')
	#start = read_file('Rotor_start_web.txt')
	arrow = read_file('Rotor_arrow_web.txt')
	
	arrow[0] = rotorIII[arrow[0]]
	arrow[1] = rotorII[arrow[1]]
	arrow[2] = rotorI[arrow[2]]
	
	#RIII_outside = read_file('outside.txt')
	#RII_outside = read_file('outside.txt')
	#RI_outside = read_file('outside.txt')
	#reflector = read_file('reflector_web.txt')
	RIII_outside, rotorIII = initial(RIII_outside, rotorIII, start[0])
	RII_outside, rotorII = initial(RII_outside, rotorII, start[1])
	RI_outside, rotorI = initial(RI_outside, rotorI, start[2])
	#input = [alphet_to_num[char] for char in input_string]
	rotorIII = rotate(rotorIII)
	RIII_outside = rotate( RIII_outside)
	if (rotorII[1] == arrow[1] and rotorIII[0] != arrow[0]) or rotorIII[0] == arrow[0]:
		rotorII = rotate(rotorII)
		RII_outside = rotate(RII_outside)
	if rotorII[0] == arrow[1]:
		rotorI = rotate(rotorI)
		RI_outside = rotate(RI_outside)

	plug = plugboard[input_value]
	   
	RIII = RIII_outside.index(rotorIII[plug])
	   
	RII = RII_outside.index(rotorII[RIII])
		 
	RI = RI_outside.index(rotorI[RII])
		   
	ref = reflector[RI]

	b_RI = rotorI.index(RI_outside[ref])
		   
	b_RII = rotorII.index(RII_outside[b_RI])
		   
	b_RIII = rotorIII.index(RIII_outside[b_RII])

	out = plugboard[b_RIII]
	
	return out