from Classes.ValveTask import ValveTask
from Classes.ValveAction import ValveAction
import copy
from datetime import datetime, timedelta
import time
import threading
import queue 

class ValveScheduler:

	def __init__(self):
			self.running: bool = False
			self.priority_queue: ValveTask = ValveTask()
			self.current_task: ValveTask = None
			self.task_queue = queue.Queue() 

	def add_new_task(self, task: ValveTask):
		self.task_queue.put(task)  # Add to the thread-safe queue

	def _add_task(self, task: ValveTask):

		queue_task = self.priority_queue

		while queue_task is not None:
			if queue_task.priority < task.priority:
				task.next = queue_task
				task.prev = queue_task.prev
				queue_task.prev = task
				break
			elif queue_task.next is None:
				queue_task.next = task
				task.prev = queue_task
				break
			else:
				queue_task = queue_task.next


	def remove_task(self, uuid: str) -> None:

		queue_task = self.priority_queue

		while queue_task is not None:
			if queue_task.id == uuid:
				queue_task.prev.next = queue_task.next
				if queue_task.next is not None:
					queue_task.next.prev = queue_task.prev
				break
			else:
				queue_task = queue_task.next

	def _find_ready_task(self):
		print("Finding Ready Task")
		queue_task = self.priority_queue
		while queue_task is not None:
			print(queue_task)
			if queue_task.is_ready(self.current_task):
				#Adjust current_task to be added to the queue
				print("Tasking Ready")
				if (self.current_task is not None):
					self.current_task.running_time = time.time() - self.current_task.execute_time
					self.current_task.execute_time = None

					temp = copy.deepcopy(self.current_task)
					self._add_task(temp)
				
				self.current_task = queue_task
				self.remove_task(queue_task.id)

				break
			else:
				print("Tasking Not Ready")
				queue_task = queue_task.next
		print("Out of loop")


	def _execute(self) -> None:
		print("Running Scheduleer")
		self.running = True
		while self.running:
			print("Runninge xecute")

			# Putting new data into the Priority queue
			while not self.task_queue.empty():
				print("Getting new task from thread queue")
				new_task = self.task_queue.get()
				self._add_task(new_task) 

			time.sleep(1)
			if self.current_task is not None:
				print(self.current_task)

			self._find_ready_task()


		
		
			
			
	def stop(self) -> None:
		#TODO: Add Pause Current Task
		self.running = False
			
	

	def start(self):
		self.running = True
		# Start the execute method in a new thread
		threading.Thread(target=self._execute, daemon=True).start()

