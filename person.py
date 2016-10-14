from random import randint

colors = [(255,255,255), (255,127,36),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),
 	(192,192,192),(128,128,128),(128,0,0),(128,128,0),(0,128,0),(128,0,128),(0,128,128),(0,0,128)]

minIntervalSeconds = 300     # 5 minutes
maxIntervalSeconds = 3600    # 1 hour

class Person:
	def __init__(self,sim,name):
		self.id = sim.personId
		self.sim = sim
		self.name = name
		self.active = True
		self.visible = True
		self.time = 0

		# Person comes in on the first floor
		startFloor = 0

		endFloor = startFloor
		while (endFloor == startFloor):
			endFloor = randomFloor(sim)

		self.startFloor = startFloor
		self.endFloor = endFloor
		self.speed = randint(5,50)
		self.color = randomColor()
		# Initialize off screen to right, and direction = -1 (moving to left)
		self.position = (sim.width + randint(100,500),sim.height - sim.ground)
		self.direction = -1
		self.destination = None

		# TODO: Build random events up front?

		self.printDetails()

	def tick(self,dt):
		self.time += dt

	def act(self,dt):
		# For now just walk
		self.tick(dt)

		self.walk()

	def walk(self):
		if not self.atDestination():
			p = self.position
			x = p[0]
			y = p[1]

			xNew = x + (self.direction * (self.speed/self.sim.speed)/100)
			if (x == xNew):
				xNew = x + (self.direction * 1)

			self.position = (xNew,y)
			if self.position[0] > 0:
				#self.printDetails()
				pass

	def randomAction(self):
		print "Doing a random action for " + self.getName()

	def atDestination(self):
		return self.position == self.destination

	def setDestination(self,destination):
		self.destination = destination

	def getDestination(self):
		return self.destination

	def printDetails(self):
		print "Name=" + self.name + " Id=" + str(self.id) + " Speed=" + str(self.speed) + " Position=" + str(self.position) + " Direction=" + str(self.direction) + " Destination=" + str(self.destination)

	def getId(self):
		return self.id

	def getName(self):
		return self.name

	def getColor(self):
		return self.color

	def getPosition(self):
		return self.position

	def enterBuilding(self):
		print self.name + " has entered building - start="+ str(self.startFloor) + ", end=" + str(self.endFloor)

	def leaveBuilding(self):
		print self.name + " has left building"

	def enterElevator(self,elevator):
		print self.name + " has entered elevator " + str(elevator.number)
		self.visible = False

	def leaveElevator(self):
		print + self.name + " has left elevator " + str(elevator.number)
		self.visible = True

		#TODO: Set floor

	# These two might not be needed after all
	def enterFloor(self):
		self.visible = False

	def leaveFloor(self):
		self.visible = True

	def randomAct(self):
		print "Doing a random act for person "

def randomFloor(sim):
	return randint(0,sim.building.numFloors)

def randomColor():
	return colors[randint(0,len(colors)-1)]