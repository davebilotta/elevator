from person import Person
from elevator import Elevator

class Building:

	def __init__(self,sim):
		print "Initializing building"
		self.sim = sim
		self.numFloors = 10
		self.numElevators = 4
		self.elevators = []
		self.floorDistance = 75

	def initElevators(self):
		e = 100

		# Don't 0-index these
		for i in range(1, self.numElevators+1):
			self.elevators.append(Elevator(i,self.sim,e))
			e+=150

	def systemEvent(self):
		print "System event - make elevator go to floor. Eventually shut down elevator"

		for elevator in self.elevators:
			if elevator.active == False:
				elevator.activate()
				return

		e = randint(0,self.numElevators-1)
		self.elevators[e].deactivate()

	def callElevator(self,floor):
		# This will call the elevator
		# What does this need to do for the building? Nothing for now

		# Add request to ECS
		self.sim.ecs.callElevator(floor)
