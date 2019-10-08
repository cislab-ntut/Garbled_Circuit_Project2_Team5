import os
import sys 

class NAND:
	"""docstring for ClassName"""
	def __init__(self,a,b):
		self.input1 = a
		self.input2 = b
	def cal(self,a,b):
		if a ==1 and b == 1:
			return 0
		else:
			return 1

class Gate(NAND):
	def __init__(self,input1,input2,gateName):
		super().__init__(input1,input2)
		self.gateName = gateName
	def call(self):	
		if self.gateName == 'XOR':
			_input1 = self.cal(self.input1,self.input1)
			_input2 = self.cal(self.input2,self.input2)
			r1 = self.cal(_input1,self.input2)
			r2 = self.cal(self.input1,_input2)
			r3 = self.cal(r1,r2)
			return r3
		elif self.gateName == 'NOT' or self.gateName == 'NAND':
			r1 = self.cal(self.input1,self.input2)
			return r1
		elif self.gateName == 'AND':
			r1 = self.cal(self.input1,self.input2)
			r2 = self.cal(r1,r1)
			return r2	
		elif self.gateName == 'OR' or 'NOR':
			r1 = self.cal(self.input1,self.input1)
			r2 = self.cal(self.input2,self.input2)
			r3 = self.cal(r1,r2)

			if self.gateName == 'NOR':
				r4 = self.cal(r3,r3)
				return r4
			else:
				return r3

NANDList = list()
NotList = list()
ANDList = list()
NORList = list()
ORList = list()
XORList = list()


for i in range(2):
	a = Gate(i,i,'NOT')
	NotList.append(a.call())


for i in range(2):
	for j in range(2):
		a = Gate(i,j,'AND')
		ANDList.append(a.call())
		b = Gate(i,j,'OR')
		ORList.append(b.call())
		c = Gate(i,j,'XOR')
		XORList.append(c.call())
		d = Gate(i,j,'NAND')
		NANDList.append(d.call())
		e = Gate(i,j,'NOR')
		NORList.append(e.call())


print('%11s' % 'a =','[0, 0, 1, 1]')
print('%11s' % 'b =','[0, 1, 0, 1]')
print('%-11s' % 'NAND Gate ',NANDList)
print('%-11s' % ' Not Gate ',NotList)
print('%-11s' % ' AND Gate ',ANDList)
print('%-11s' % ' NOR Gate ',NORList)
print('%-11s' % ' OR  Gate ',ORList)
print('%-11s' % ' XOR Gate ',XORList)



