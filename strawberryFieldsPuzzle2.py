# -*- coding: utf-8 -*-
# Karen West
# Rewriting strawberry fields puzzle:
# Originally written for ITA Google in Aug. 2011 in C, to attempt to get
# an interview there (did not! ;-)), rewritten after learning Python in 
# 2012-2013, and someone recently recommended that if I want to turn it 
# into an application, I should re-write it in Ruby since I am in the process 
# of learning Rails.  Otherwise, I would also have to learn Django if I 
# wanted to make it into an app with Python, an option too, since the 
# app deployment tool, called Heroku, deploys both Python and Ruby apps.  
# Someone also said I should learn to make apps in Android, even though I do 
# not yet own an Android device - some ADK (Android Development Kit?) that 
# you can run on your computer as a virtual machine that runs Android and 
# helps you to make their apps.  For now-- just trying to get an old puzzle
# to work in Python, since I know that better than Ruby. ;-)

# One of the many exercises I am doing to build skills for employment!

import math
import random

#import ps7_visualize #can I use this for the strawberry fields project?
#import pylab

STRAWBERRY_FIELD_FILENAME = "StrawberryFieldsPuzzleEx.in"
MAXROWS = 50
MAXCOLS = 50
GREENHOUSE_LETTER_VALUES = {
    0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D', 4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H', 8 : 'I', 9 : 'J', 10 : 'K', 11 : 'L', 12 : 'M', 13 : 'N', 14 : 'O', 15 : 'P', 16 : 'Q', 17 : 'R', 18 : 'S', 19 : 'T', 20 : 'U', 21 : 'V', 22 : 'W',23 : 'X', 24 : 'Y', 25 : 'Z'
}
GREENHOUSE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class strawBerryFieldsListClass(object):
    """
    a list of 2-dimensional strawberry fields
    """
    def __init__(self):
        print "initializing strawBerryFieldsListClass"

        self.strawberryFieldsList = []
        self.numStrawberryFields = 0

    def getStrawberryFieldsList(self):
        return self.strawberryFieldsList

    def setStrawberryFieldsList(strawbFieldList):
        self.strawberryFieldsList = strawbFieldList

    def getNumStrawBerryFields(self):
        return self.numStrawberryFields

    def setNumStrawBerryFields(num):
        self.numStrawberryFields = num

def displayStrawberryField(aStrawberryField):
    numRows = aStrawberryField.rows
    numCols = aStrawberryField.cols
    for x in range(numRows):
        for y in range(numCols):
            if (aStrawberryField.strawberryField[x][y] == '@'):
                print "strawb here: x,y"
                print x
                print y
            print aStrawberryField.strawberryField[x][y]

def displayGreenHouseField(aStrawberryField):
    numRows = aStrawberryField.rows
    numCols = aStrawberryField.cols
    for x in range(numRows):
        print "row " + str(x)
        for y in range(numCols):
            print aStrawberryField.strawberryFieldWithGreenHouses[x][y]

def loadArrangeStrawberryFields():
        """
        loads strawberryFields and arranges them in the data structure so 
        the strawberries can be covered by green houses.

        Initially, the entire field is just empty locations (periods) or 
        contains a strawberry (@).  (Later, the strawberries will be replaced 
        by the optimal number of greenhouses).
        """
        print "Loading matrice list from file..."
        # inFile: file
        print "opening file to get strawberry fields"
        inFile = open(STRAWBERRY_FIELD_FILENAME, 'r', 0)
        countRows = 0
        #strawberryFieldsListObj = strawBerryFieldsListClass()
        #strawberryFieldsList = strawberryFieldsListObj.getStrawberryFieldsList()
        #print "init - num strawb fields should be zero"
        #print strawberryFieldsList[0].numStrawberryFields
        strawberryFieldsList = []
        numStrawberryFields = 0
        aStrawberryField = StrawberryFieldClass()
        numGreenHouseMax = 0        
        strawberryFieldRowStr = ""
        print "processing each line of strawberry field"
        for line in inFile:
            print line
            print "row" + str(countRows)
            strawberryFieldRowStr = line.strip().lower()
            if (countRows == 0):
                numGreenHousesMax = int(strawberryFieldRowStr[0])
                print "max num green houses"
                print numGreenHousesMax
                #print "count rows went from 0 to 1"
                countRows += 1
                #now that you know the max number of green houses, init the list of green house letters
                for greenHouseNum in range(numGreenHousesMax):
                    #print "forming green house letter representation"
                    aStrawberryField.greenHouseLetterList.append(GREENHOUSE_LETTER_VALUES[greenHouseNum])
            elif (countRows <> 0) and (strawberryFieldRowStr[0] != ' '): #still in same Strawberry Field
                #print "count rows <> 0"
                for colNum in range(len(strawberryFieldRowStr)):
                    aStrawberryField.strawberryField[countRows - 1][colNum] = strawberryFieldRowStr[colNum]
                    aStrawberryField.strawberryFieldWithGreenHouses[countRows - 1][colNum] = strawberryFieldRowStr[colNum]
                    if (strawberryFieldRowStr[colNum] == '@'):
                        aStrawberryField.numStrawberriesInField += 1
                if (countRows == 1):
                    aStrawberryField.cols = len(strawberryFieldRowStr)
                    aStrawberryField.numGreenHousesMax = numGreenHousesMax
                    countRows += 1
                else:
                    countRows += 1
                strawberryFieldRowStr = ""
            #else: #end of this strawberry field - add to list of strawberry fields
        #if (strawberryFieldRowStr[0] == ' '):
        print "just loaded strawberry field"
        #print aStrawberryField
        aStrawberryField.rows = countRows - 1
        print "rows"
        print aStrawberryField.rows
        print "cols"
        print aStrawberryField.cols
        strawberryFieldsList.append(aStrawberryField)
        numStrawberryFields += 1
        countRows = 0
        strawberryFieldRowStr = ""
        aStrawberryField = StrawberryFieldClass()
        #strawberryFieldsListObj.setStrawberryFieldsList(strawberryFieldsList)
        #strawberryFieldsListObj.setNumStrawberryFields(numStrawberryFields)
        return strawberryFieldsList

class StrawberryFieldClass(object):
    """
    A two-dimensional strawberry field.
    
    A (Rectangular) StrawberryField represents a rectangular region 
    containing @ symbols as strawberries within the field, and the rest of 
    the field has dots or periods "."

    A strawberry field has a width(numCols) and a height(numRows) and 
    contains (width * height) locations for strawberries.
    At any particular time, each of these locatins is either occupied by a 
    strawberry or not.
    """

    def __init__(self):
        """
        Initializes a position with coordinates (x, y).
        """
        # You have to first initialize the outer list with lists before adding items:
        # Creates a list containing 5 lists initialized to 0
        # Matrix = [[0 for x in xrange(5)] for x in xrange(5)]         
        # OR Matrix = [[0 for i in range(5)] for j in range(5)]

        # So--not sure how big our strawberry fields will be--so init to be a max size instead
        
        self.strawberryField = [[False]*MAXROWS for _ in range(MAXCOLS)]
        self.strawberryFieldWithGreenHouses = [[False]*MAXROWS for _ in range(MAXCOLS)]
        self.rows = 0
        self.cols = 0
        self.numStrawberriesInField = 0
        self.numStrawberriesCoveredInField = 0
        self.strawberryPositionsCoveredList = []
        self.noStrawberryPositionsList = []
        self.numGreenHousesMax = 0
        self.greenHouseCount = 0
        self.greenHouseLetterList = []
        self.numFieldLocsVisited = 0

    def getNumFieldLocsVisited(self):
        return self.numFieldLocsVisited
        
    def getRows(self):
        return self.rows
    
    def getCols(self):
        return self.Cols

    def getStrawberryField(self):
        return self.strawberryField

    def getGreenHouseField(self):
        return self.strawberryFieldWithGreenHouses

    def getNumGreenHouses(self):
        return self.numGreenHouses
    
    def coverStrawberryWithGreenHouseAtPosition(self, pos):
        """
        HAVE NOT FIGURED OUT YET: how to determine which greenHouse letter to cover strawberry with!!
        Perhaps do that later! (?? fitNumGreenHousesToStrawberryField() ??)

        Cover the strawberry under the position POS as with greenhouse letter specified.

        Assumes that POS represents a valid position inside the green house.

        pos: a Position
        """
        x = int(pos.getX())
        y = int(pos.getY())
        print "x pos and y pos"
        print x
        print y
        if ((x,y) in self.strawberryPositionsCoveredList):
            print "strawberry already covered!"
            return
        elif ((x,y) in self.noStrawberryPositionsList):
            print "already visited this strawberry field location - no strawberry here!"
        else: #have not visited this strawberry field location before
            self.numFieldLocsVisited += 1
            if self.strawberryField[x][y] == '@':
                print "strawberry located here! append to list so can cover with gh later"
            #self.strawberryFieldWithGreenHouses[x][y] = self.strawberryField.greenHouseLetterList.append(GREENHOUSE_LETTER_VALUES[self.greenHouseCount])
                self.strawberryPositionsCoveredList.append((x,y)) #use for rearranging green house letters later
                self.numStrawberriesCoveredInField += 1
                #if total gh's = 4, and total strawbs = 43, then to start,
                #keeping it simple - divide equally, strawbs to gh's, rather
                #then based on proximity of location for now
                #43/11 = rounds to 4, 43/22 rounds to 2, 43/33 rounds to 1,
                #43/44 rounds to < 1.
                #so to start - do first 11 wit gh A, next 11 gh B, etc.
                self.fitNumGreenHousesToStrawberryField(x,y)
            else:
                print "no strawberry located here!"
                self.noStrawberryPositionsList.append((x,y))

    def fitNumGreenHousesToStrawberryField(self,x,y):
        """
        figure out later! constrained by the maximum allowed number of greenhouses, and where they are
        located in the strawberry field
        ----look at strawberryPositionsCoveredList to arrange and fit the max number of green houses
        ----how many strawberries covered?

---since I last looked at this in Dec 2012 - it's now June 2013 - perhaps
once you build the list of strawberry locations, you can use some of the AI
cost techniques to figure out the greenhouse coverage - ?? -
bfs, dfs, a-star, uniform cost, etc


        ??? could it be as I originally thought about it in C in Aug. 2011, where now is the time to build
        a tree of nodes that are connected to each other, to determine the best cost of covering them with
        a greenhouse?  Using either depth-first-search OR breadth-first-search, and even when there are gaps
        between strawberries, meaning there are periods/dots between them, sometimes they must be part of the
        same greenHouse, based on the contraint that you only are given a maximum amount of greenHouses to cover
        the sometimes sparsely populated strawberry patches in the strawberry field?  Other times, you don't need
        as many as the maximum you are given.  In the cases where you don't have enough green houses to cover your
        strawberries with no dots/periods in bewteen them, calculate the cost or distance of using one greenhouse
        over another??   build it in a dictionary?
        """
        numGreenHousesLeft = self.numGreenHousesMax - self.greenHouseCount
        print "num gh left to use for covering " + str(numGreenHousesLeft)
        print "green house count so far " + str(self.greenHouseCount)
        factor = int(round(self.numStrawberriesInField / self.numGreenHousesMax ))
        print "factor " + str(factor)
        numPositionsCovered = self.numStrawberriesCoveredInField
        print "num pos covered with gh's"
        print numPositionsCovered
        anyRemainder = numPositionsCovered % factor
        factorCovered = round(numPositionsCovered / factor)
        #if no remainder then increment gh number
        #keep simple to start! cover with position in grid in mind later
        print "num green houses left to use for covering strawberries " + str(numGreenHousesLeft)
        print "factor covered:" + str(factorCovered)
        print "anyRemainder = numPositionsCovered % factor " + str(anyRemainder)
        if (anyRemainder) and (factorCovered == (self.greenHouseCount)):
            self.greenHouseCount += 1
        print self.isStrawberryCoveredWithGreenHouse(x,y)
        if (self.strawberryField[x][y] == '@') and (not self.isStrawberryCoveredWithGreenHouse(x,y)) :
            print "covering strawb with gh at x,y = "
            print x
            print y
            print 
            print "green house count " + str(self.greenHouseCount)
            print "green house letter " + GREENHOUSE_LETTER_VALUES[self.greenHouseCount - 1]
            self.strawberryFieldWithGreenHouses[x][y] = GREENHOUSE_LETTER_VALUES[self.greenHouseCount - 1]
            print "green house letter just used to cover this strawberry"
            print self.strawberryFieldWithGreenHouses[x][y]
        

    def isStrawberryCoveredWithGreenHouse(self, m, n):
        """
        Return True if the strawberry field location (m, n) has been covered with a green house.

        Assumes that (m, n) represents a valid strawberry field location inside the strawberry field.

        m: an integer
        n: an integer
        returns: True if (m, n) is covered with a green house, False otherwise
        """
        print "strawberryFieldWithGreenHouses"
        print "loc x,y"
        print m
        print n

        if str(self.strawberryFieldWithGreenHouses[m][n]) in GREENHOUSE_LETTERS:
            print "greenhouse letter for this loc"
            print self.strawberryFieldWithGreenHouses[m][n]
            return True
        else:
            print "no green house letter in this location"
            print self.strawberryFieldWithGreenHouses[m][n]
            return False
    
    def getTotalNumStrawberryFieldLocations(self):
        """
        Return the total number of locations in field where a strawberry could be located.

        returns: an integer
        """
        return self.rows * self.cols

    def getNumCoveredStrawberries(self):
        """
        Return the total number of covered strawberries in field.

        returns: an integer
        """
        return self.numStrawberriesCoveredInField

    def getNumStrawberriesinField(self):
        """
        Return the total number of strawberries in field.

        returns: an integer
        """
        return self.numStrawberriesInField

    def getRandomPosition(self):
        """
        Return a random position inside the strawberry field position.

        returns: a Position object.
        """
        x = random.random() * self.rows
        y = random.random() * self.cols
        return Position(x, y)

    def isPositionInStrawberryField(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        test_x = 0 <= pos.getX() < self.rows
        test_y = 0 <= pos.getY() < self.cols
        print "true if pos is in room"
        print test_x and test_y
        return test_x and test_y
    
# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional strawberry field.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        #print "new x = " + str(new_x) + " new y " + str(new_y)
        #print "floor of x = " + str(math.floor(new_x)) + " floor of y = " + str(math.floor(new_y))
    
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)

class GreenHouseWorker(object):
    """
    Represents a person covering a strawberry field with a green house.

    At all times the greenHouse Covering Person has a particular position and direction in the room.
    The green house covering person also has a fixed speed.

    Subclasses of green house covering person should provide movement strategies by implementing
    updatePositionAndCoverStrawberry(), which simulates a single time-step.
    """
    def __init__(self, strawberryField, speed):
        """
        Initializes a green house covering person with the given speed in the specified strawberry field.
        The green house covering person initially has a random direction and a random position in the
        strawberry field. The green house covering person covers the location in the field with a green houses        letter when it is on that location, if it contains a strawberry.

        strawberryField:  a StrawberryField object.
        speed: a float (speed > 0) - the speed that the green house covering person covers strawberries with a greenhouse
        """
        self.strawberryField = strawberryField
        self.speed = speed
        self.direction = int(random.random() * 360)
        self.position = strawberryField.getRandomPosition()
        strawberryField.coverStrawberryWithGreenHouseAtPosition(self.position)

    def getGreenHouseWorkerPosition(self):
        """
        Return the position of the green house cover person.

        returns: a Position object giving the green house cover person's position.
        """
        return self.position
    
    def getGreenHouseWorkerDirection(self):
        """
        Return the direction of the green house cover person.

        returns: an integer d giving the direction of the green house cover person as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setGreenHouseWorkerPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setGreenHouseWorkerDirection(self, direction):
        """
        Set the direction of the green house cover person to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndCoverStrawberryWithGH(self):
        """
        Simulate the raise passage of a single time-step.

        Move the green house cover person to a new position and mark the 
        strawberry field location it is on as having
        been covered with a green house.
        """
        raise NotImplementedError # don't change this!

# === Problem 2
class StandardGHworker(GreenHouseWorker):
    """
    A StandardGreenHouseWorker is a GreenHouseWorker with the standard 
    movement strategy.

    At each time-step, a StandardGreenHouseWorker attempts to move 
    in its current direction; when it would hit the end of the strawberry 
    field, it *instead* chooses a new direction randomly.
    """
    def updatePositionAndCoverStrawberryWithGH(self):
        """
        Simulate the raise passage of a single time-step.

        Move the green house covering person to a new position and mark the 
        strawberry field location it is on as having
        been covered with a green house.
        """
        position = self.position.getNewPosition(self.direction, self.speed)
        print "position after update" + str(position)
        if self.strawberryField.isPositionInStrawberryField(position):
            self.setGreenHouseWorkerPosition(position)
            self.strawberryField.coverStrawberryWithGreenHouseAtPosition(position)
        else:
            self.setGreenHouseWorkerDirection(int(random.random() * 360))

# === Problem 3
def numGHsForStrawberryField(num_ghWorkers, speed, width, height, min_coverage, num_trials, gh_workerType):
    """
    Strawberry Fields Puzzle Problem Description:

    Strawberries are growing in a rectangular field of length and width at 
    most 50. You want to build greenhouses to enclose the strawberries. 
    Greenhouses are rectangular, axis-aligned with the field 
    (i.e., not diagonal), and may not overlap. The cost of each greenhouse 
    is $10 plus $1 per unit of area covered.

    Write a program that chooses the best number of greenhouses to build, and 
    their locations, so as to enclose all the strawberries as cheaply as 
    possible. Heuristic solutions that may not always produce the 
    lowest possible cost will be accepted: seek a reasonable tradeoff 
    of efficiency and optimality.

    Your program must read a small integer 1 ≤ N ≤ 10 representing the 
    maximum number of greenhouses to consider, and a matrix representation of 
    the field, in which the '@' symbol represents a strawberry. Output 
    must be a copy of the original matrix with letters used to represent 
    greenhouses, preceded by the covering's cost. 

    Here is an example input-output pair:

    Input	 	
    4
    ..@@@@@...............
    ..@@@@@@........@@@...
    .....@@@@@......@@@...
    .......@@@@@@@@@@@@...
    .........@@@@@........
    .........@@@@@........

    Output
    90
    ..AAAAAAAA............
    ..AAAAAAAA....CCCCC...
    ..AAAAAAAA....CCCCC...
    .......BBBBBBBCCCCC...
    .......BBBBBBB........
    .......BBBBBBB........

    In this example, the solution cost of $90 is computed as 
    (10+8*3) + (10+7*3) + (10+5*3). 

    Run your program on the 9 sample inputs found in this file and report 
    the total cost of the 9 solutions found by your program, as well as each 
    individual solution.
 
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to cover the strawberries with green houses, 
    MIN_COVERAGE of the strawberry field.

    The simulation is run with NUM_GHworkers of type GHworker_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_ghWorkers: an int (num_ghWorkers > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    ghWorker_type: class of green house worker to be instantiated 
     (e.g. StandardGHworker or RandomGHworker)
    """
    greenHouseList = []
    
    #strawberryFieldsListObj = strawBerryFieldsListClass()
    #print "initializing a strawberry field class"
    #aStrawberryField = StrawberryFieldClass() 
    print "now calling the loading of strawberry fields"
    
    strawberryFieldsList = loadArrangeStrawberryFields()
    #print strawberryFieldsList
    #strawberryField = strawberryFieldsList[0]
    
    #strawberryFieldsList = strawberryFieldsListObj.getStrawberryFieldsList()

    for strawberryField in strawberryFieldsList:
        displayStrawberryField(strawberryField)
        if (gh_workerType == 0): #standard green house worker
            ghWorker = StandardGHworker(strawberryField, speed)
            print "just initialiazed a green house worker"
        steps = 0
        for _ in range(num_trials):
            ghWorkerList = []
            for _ in range(num_ghWorkers):
                ghWorkerList.append(ghWorker)
                print "gh worker appended to list"
                total_fieldLocations = float(strawberryField.getTotalNumStrawberryFieldLocations())
                print "total field locations"
                print total_fieldLocations
                print "number of covered strawberries"
                print strawberryField.getNumCoveredStrawberries()
                while strawberryField.getNumFieldLocsVisited() / total_fieldLocations < min_coverage:
                    print "determines whether every loc in field has been visited once"
                    print strawberryField.getNumFieldLocsVisited() / total_fieldLocations
                    steps += 1
                    print "number of covered strawberries"
                    print strawberryField.getNumCoveredStrawberries()
                    print "steps " + str(steps)
                    print "about to get a gh worker to cover strawb with gh"
                    for ghworker in ghWorkerList:
                        print "about to updatePositionAndCoverStrawberryWithGH"
                        ghworker.updatePositionAndCoverStrawberryWithGH()
                    print "determines whether every loc in field has been visited once"
                    print strawberryField.getNumFieldLocsVisited() / total_fieldLocations
         
        displayGreenHouseField(strawberryField)
    return steps / float(num_trials)

# === Problem 4
class RandomWalkGHworker(GreenHouseWorker):
    """
    A RandomWalkGHworker is a green house worker with the "random walk" 
    movement strategy: it chooses a new direction at random at the end of 
    each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the green house worker to a new position and mark the field
        location it is on as having been checked to see if there is a
        strawberry there that needs covering with a green house.
        """
        position = self.position.getNewPosition(self.direction, self.speed)
        if self.field.isPositionInRoom(position):
            self.setFieldPosition(position)
            self.field.coverStrawberryAtPosition(position)
        self.setGHworkerDirection(int(random.random() * 360))
