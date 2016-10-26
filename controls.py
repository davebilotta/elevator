# Control Systems go here - contains ElevatorControlSystem (and others?)

class ElevatorControlSystem:

	def __init__(self,sim):
		print "Initializing Elevator Control System (ECS)"
		self.sim = sim
		self.numElevators = 4
		self.elevators = []
		self.requests = {}

		for floor in range(0,self.sim.building.numFloors+1):
			self.requests[floor] = 0

	def initElevators(self):
		self.elevators = self.sim.building.elevators

	def callElevator(self,floor):
		# This will call the elevator
		self.addRequest(floor)

	def addRequest(self,floor):
		print "ECS - Added request for elevator on floor " + str(floor)
		req = self.requests[floor]
		req += 1

		self.requests[floor] += 1
		print str(self.requests)

	def clearRequests(self,floor):
		print "Requests cleared on floor " + str(floor)
		self.requests[floor] = 0

	def getClosestElevator(self,floor):
		#print "Finding closest elevator to floor " + str(floor)

		closest = None
		distance = self.sim.building.numFloors
		for elevator in self.elevators:
			if elevator.active:
				d = abs(elevator.floor - floor)
				print "Distance between elevator " + str(elevator.number) + " (currently on floor " + str(elevator.floor) + ") and floor " + str(floor) + " is " + str(d)

				if (d < distance):
					closest = elevator
					distance = d

		# Need to handle case where no elevator is active and we can't find one
		if closest:
			print "Closest elevator to floor " + str(floor) + " is " + str(closest.number)

