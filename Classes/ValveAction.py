from typing import TypedDict, Literal


OperationType = Literal[1, 0]

class ValveActionData(TypedDict):
	operation: OperationType
	id: int

class ValveAction:
	def __init__(self, data):
		if data == None:
			return
		self.operation: OperationType = data['operation']
		self.id = data['id']