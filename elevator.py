from random import randint

class Elevator:

	def __init__(self,number,sim,xpos):
		self.number = number
		self.sim = sim
		self.tick = 0

		# Set floor and position
		floor = randint(1,sim.building.numFloors)
		self.floor = floor
		self.position = (xpos,(sim.height-sim.ground - (floor * sim.building.floorDistance)))

		self.destination = None
		self.location = None
		self.size = (70,70)
		self.capacity = 20
		self.persons = []              # These are the people in the Elevator

		print "Initializing elevator " + str(number) + " at " + str(self.position) + " on floor " + str(floor)

		self.activate()
		self.stop()
		self.close()

	def act(self,dt):
		self.tick += dt
		# For each person in self.persons, once we're at floor call their addQueuedEvent method to set floor

	def setFloor(self,floor):
		print "Setting elevator " + str(self.number) + " to floor " + str(floor)
		self.floor = floor
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

	def isActive(self):
		return self.active

	def isMoving(self):
		return self.moving

	def getFloor(self):
		return self.floor

	def arrive(self):
		self.sim.announce(True)

	def depart(self):
		self.sim.announce(False)