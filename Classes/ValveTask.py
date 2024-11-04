from Classes.ValveAction import ValveActionData, ValveAction
from typing import List, TypedDict, Optional
import sys
from uuid import uuid4
import time


class ValveTaskData(TypedDict):
	request_time: str
	priority: int
	actions: List[ValveActionData]
	start_time: str
	running_time: str

class ValveTask:

	def __init__(self, data: ValveTaskData = None):
		print("IN Vavle Task -------")
		print(data)
		self.execute_time: Optional[int] = None
		self.next: Optional['ValveTask'] = None
		self.prev: Optional['ValveTask'] = None
		self.request_time = None
		self.actions = []
		self.running_time = 0

		if data == None:
			self.priority: int = sys.maxsize
			self.start_time: int = sys.maxsize
			self.id = "Head"
			return
		
		self.id = uuid4()
		self.priority = data['priority']
		if self.priority < 0 or self.priority == sys.maxsize:
			raise ValueError("Invalid operation")
		
		self.request_time: int = data['request_time']
		self.actions: List[ValveAction] = list(map(lambda action: ValveAction(action), data['actions']))
		self.running_time = data['running_time']
		self.start_time = data['start_time']


	def is_ready(self, current_task: 'ValveTask') -> bool:

		
		if time.time() >= self.start_time:
			if current_task is None:
				return True
			if self.priority > current_task.priority:
				return True
			
		return False
		



	def print_queue(self):
		queue_task = self
		while queue_task is not None:
			print(queue_task)
			queue_task = queue_task.next
		

	def __str__(self):
		return f"ValveTask(id={self.id}, priority={self.priority}, request_time={self.request_time}, actions={[action.operation for action in self.actions]})"
