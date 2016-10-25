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
		self.requests = {}

		for floor in range(0,self.numFloors+1):
			self.requests[floor] = 0


	def initElevators(self):
		e = 100

		# Don't 0-index these
		for i in range(1, self.numElevators+1):
			self.elevators.append(Elevator(i,self.sim,e))
			e+=150

	def systemEvent(self):
		print "System event - make elevator go to floor. Eventually shut down elevator"

		for elevator in self.elevators:
			if elevator.activeStatus() == False:
				elevator.activate()
				return

		e = randint(0,self.numElevators-1)
		self.elevators[e].deactivate()

	def callElevator(self,floor):
		# This will call the elevator
		self.addRequest(floor)

	def addRequest(self,floor):
		print "Added request for elevator on floor " + str(floor)
		req = self.requests[floor]
		req += 1

		self.requests[floor] += 1
		print str(self.requests)

	def clearRequests(self,floor):
		print "Requests cleared on floor " + str(floor)
		self.requests[floor] = 0

	def getElevators(self):
		return self.elevators