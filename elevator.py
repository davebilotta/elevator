from random import randint

class Elevator:

	def __init__(self,number,sim,xpos):
		self.number = number
		self.sim = sim
		floor = randint(1,sim.building.numFloors)

		self.position = (xpos,(sim.height-sim.ground - (floor * sim.building.floorDistance)))
		#self.setFloor(floor)

		self.destination = None
		self.location = None
		self.size = (70,70)
		self.capacity = 20

		print "Initializing elevator " + str(number) + " at " + str(self.position) + " on floor " + str(floor)

		self.activate()
		self.stop()
		self.close()

	def setFloor(self,floor):
		print "Setting elevator " + str(self.number) + " to floor " + str(floor)
		self.position = (self.position[0],(self.sim.height-self.sim.ground - (floor * self.sim.building.floorDistance)))

	# Active
	def activate(self):
		self.active = True
		print "Elevator is active"

	def deactivate(self):
		self.active = False

	def activeStatus(self):
		return self.active

	# Moving
	def start(self):
		self.moving = True
		print "Elevator " + str(self.number) + " is moving"

	def stop(self):
		self.moving = False
		print "Elevator " + str(self.number) + " has stopped"

	# Doors open/close
	def open(self):
		self.doorsOpen = True

	def close(self):
		self.doorsOpen = False

	def getNumber(self):
		return self.number

	def getPosition(self):
		return self.position

	def getSize(self):
		return self.size

	def getCapacity(self):
		return self.capacity