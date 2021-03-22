import random

class Noeud:
	def __init__(self):
		self.__color = random.choice(['red','green','blue', 'orange', 'yellow', 'purple', 'gray'])
		self.__neighbours = []
		return None

	def get_color(self):
		return self.__color