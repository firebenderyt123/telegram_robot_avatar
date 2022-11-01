class Queue:

	_queue = []

	def __init__(self, queue = []):
		self._queue = queue

	def push_back(self, elem):
		if elem not in self._queue:
			self._queue.append(elem)

	def insert(self, pos, elem):
		if elem not in self._queue:
			self._queue.insert(pos, elem)

	def replace(self, elem, replace_with):
		for i, e in enumerate(self._queue):
			if e == elem:
				self._queue[i] == replace_with
				break

	def get_queue(self):
		return self._queue

	def get_length(self):
		return len(self._queue)

	def get_elem(self, pos = 0):
		if pos < len(self._queue):
			return self._queue[pos]
		else:
			return None

	def remove_elem(self, pos = 0):
		if pos < len(self._queue):
			self._queue.pop(pos)