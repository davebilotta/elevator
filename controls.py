#

class ElevatorControlSystem:

	def __init__(self,sim):
		print "Initializing Elevator Control System (ECS)"
		self.sim = sim
		self.numElevators = 4
		self.elevators = []

	def initElevators(self):
		self.elevators = self.sim.building.getElevators()

	def getClosestElevator(self,floor):
		#print "Finding closest elevator to floor " + str(floor)

		closest = None
		distance = self.sim.building.numFloors
		for elevator in self.elevators:
			if elevator.isActive():
				d = abs(elevator.getFloor() - floor)
				print "Distance between elevator " + str(elevator.getNumber()) + " (currently on floor " + str(elevator.getFloor()) + ") and floor " + str(floor) + " is " + str(d)

				if (d < distance):
					closest = elevator
					distance = d

		# Need to handle case where no elevator is active and we can't find one
		if closest:
			print "Closest elevator to floor " + str(floor) + " is " + str(closest.getNumber())

