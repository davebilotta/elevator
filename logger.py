class MessageLogger:
	def __init__(self,sim):
		self.sim = sim
		self.messages = []
		self.max_messages = 100

	def log(self,message):
		self.messages.append(message)