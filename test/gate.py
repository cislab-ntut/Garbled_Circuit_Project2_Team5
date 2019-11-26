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





