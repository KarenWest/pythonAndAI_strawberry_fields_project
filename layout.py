 # layout.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Grid
import os
import random
"""    
    Here is an example input-output pair:

    Input (@ = strawberry, . = location in strawberry field with no strawberry in it, first line number = maximum allowed greenhouses)	 	
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
     $10 for each greenhouse
     greenhouse A is 8x3, greenhouse B is 7x3, and greenhouse C is 5x3
     so cost is:
    (10+8*3) + (10+7*3) + (10+5*3). 

    left off at:
    in search.py -- when you call the various dfs, bfs, aStarSearch and ucs,
    somehow have to incorporate the locations of these strawberries in the
    layout to the cost functions calculated for these search trees in
    search.py

Reads in as this:
max greenhouses read in for this field: 4
processLayoutText
['%%%%%%%%%%%%%%%%%%%%%%%%', '%..@@@@@...............%', '%..@@@@@@........@@@...%', '%.....@@@@@......@@@...%', '%.......@@@@@@@@@@@@...%', '%.........@@@@@........%', '%.........@@@@@........%', '%%%%%%%%%%%%%%%%%%%%%%%%']

self.food - which contains T = True for where strawberries are located,
and F = False for locations in field where there are no strawberries.
--->Grid structure is upside down to the list and field display above:

total strawberries in this field = 44
FFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFTTTTTFFFFFFFFF
FFFFFFFFFFTTTTTFFFFFFFFF
FFFFFFFFTTTTTTTTTTTTFFFF
FFFFFFTTTTTFFFFFFTTTFFFF
FFFTTTTTTFFFFFFFFTTTFFFF
FFFTTTTTFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFF

"""
VISIBILITY_MATRIX_CACHE = {}
GREENHOUSE_LETTER_VALUES = {
    0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D', 4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H', 8 : 'I', 9 : 'J', 10 : 'K', 11 : 'L', 12 : 'M', 13 : 'N', 14 : 'O', 15 : 'P', 16 : 'Q', 17 : 'R', 18 : 'S', 19 : 'T', 20 : 'U', 21 : 'V', 22 : 'W',23 : 'X', 24 : 'Y', 25 : 'Z'
}
def getLayout(name, back = 2):
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout == None: layout = tryToLoad(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout == None: layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back -1)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname):
    if(not os.path.exists(fullname)): return None
    f = open(fullname)
    count = 0
    restOfLines = []
    for line in f:
        if (count == 0):
            line1 = line.strip()
            maxGHs = line1[0]
            print "max greenhouses read in for this field: " + str(maxGHs)
            count += 1
        else:
            if (line.strip() != ''):
                restOfLines.append(line.strip())
    print "strawberry field with max greenhouses removed from 1st line"
    print restOfLines
    try: return Layout(restOfLines, int(maxGHs))
    finally: f.close()

def displayStartLoc(currentY, currentX, startLocYBefore, startLocXBefore, startLocYAfter, startLocXAfter):
    print "current loc"
    print currentY
    print currentX
    print "modify start - pos before"
    print startLocYBefore
    print startLocXBefore
    print "pos afterward"
    print startLocYAfter
    print startLocXAfter

def displayEndLoc(currentY, currentX, endLocYBefore, endLocXBefore, endLocYAfter, endLocXAfter):
    print "current loc"
    print currentY
    print currentX
    print "modify end - pos before"
    print endLocYBefore
    print endLocXBefore
    print "pos afterward"
    print endLocYAfter
    print endLocXAfter

class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText, maxGHs):
        self.width = len(layoutText[0])
        self.height= len(layoutText)
        print "strawberry field dimensions just read in:"
        print "width " + str(self.width)
        print "height " + str(self.height)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.strawbLocList = []
        self.numGHs = Grid(self.width, self.height, False)
        self.maxGHs = maxGHs
        self.numGHsUsed = 0
        self.numGHsNeeded = 0
        self.ghLetList = []
        self.widthGapList = [] #don't need?
        self.heightGapList = [] #don't need?
        self.strawbFieldStartLocByRowList = []
        self.strawbFieldEndLocByRowList = []
        self.numStrawbPatchStartsPerRow = {}
        self.numStrawbPatchEndsPerRow = {}
        self.ghDict = {} #key index gh letter - values locs of gh?
        self.agentPositions = []
        self.processLayoutText(layoutText)
        self.layoutText = layoutText
        self.totStrawb = 0
        self.numStrawbCov = 0
        for i in range(self.maxGHs):
            self.ghLetList.append(GREENHOUSE_LETTER_VALUES[i])
        # self.initializeVisibilityMatrix()
#self.ghLetList[self.numGHsUsed] = green house letter representation

    def initializeVisibilityMatrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
            from game import Directions
            vecs = [(-0.5,0), (0.5,0),(0,-0.5),(0,0.5)]
            dirs = [Directions.NORTH, Directions.SOUTH, Directions.WEST, Directions.EAST]
            vis = Grid(self.width, self.height, {Directions.NORTH:set(), Directions.SOUTH:set(), Directions.EAST:set(), Directions.WEST:set(), Directions.STOP:set()})
            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] == False:
                        for vec, direction in zip(vecs, dirs):
                            dx, dy = vec
                            nextx, nexty = x + dx, y + dy
                            while (nextx + nexty) != int(nextx) + int(nexty) or not self.walls[int(nextx)][int(nexty)] :
                                vis[x][y][direction].add((nextx, nexty))
                                nextx, nexty = x + dx, y + dy
            self.visibility = vis
            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def getRandomLegalPosition(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        while self.isWall( (x, y) ):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))
        return (x,y)

    def getRandomCorner(self):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        return random.choice(poses)

    def getFurthestCorner(self, ghWorkerPos):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        dist, pos = max([(manhattanDistance(p, ghWorkerPos), p) for p in poses])
        return pos

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:],self.maxGHs)

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         @ - Food
        Other characters are ignored.
        """
        print "processLayoutText"
        print layoutText
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                #print "layoutChar pos = " + str(maxY - y) + "," + str(x)
                #print "layoutChar = "
                layoutChar = layoutText[maxY - y][x]
                #print layoutChar
                self.processLayoutChar(maxY - y, x, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [ ( i == 0, pos) for i, pos in self.agentPositions]
        self.totStrawb = self.food.count()
        print "total strawberries in this field = " + str(self.totStrawb)
        print self.food
        self.strawbLocList = self.food.asList()
        print self.strawbLocList
        self.findStartAndEndOfStrawbFieldLocsByRow()        
        #self.buildStrawbFieldStartEndLocLists()
        print "list of start locs of strawbs in rows"
        print self.strawbFieldStartLocByRowList
        print "list of end locs of strawbs in rows"
        print self.strawbFieldEndLocByRowList
        print "now modifying start and end loc of strawbs by rows"
        self.modifyStrawbFieldStartEndLocLists()
        print "list of start locs of strawbs in rows"
        print self.strawbFieldStartLocByRowList
        print "list of end locs of strawbs in rows"
        print self.strawbFieldEndLocByRowList
        #numGHsNeeded = self.countStrawbFieldStartEndLocs()
        #self.findNumGHsNeeded()

    def processLayoutChar(self, y, x, layoutChar):
        #print "processLayoutChar" + str(layoutChar)
        if layoutChar == '@':
            self.food[y][x] = True
            
        self.agentPositions.append( (0, (0, 0) ) )

    def findStartAndEndOfStrawbFieldLocsByRow(self):
        maxY = self.height - 1
        print "food at start of findStartAndEndOfStrawbFieldLocsByRow"
        print self.food
        for y in range(self.height): # num rows are the height
            for x in range(self.width): # num cols are the width
                pos = (0,0)
                if (x == 0) : #start of row is col 0
                    if (self.food[(maxY - y)][x] == True): #if start of row has strawb
                        #print "col 0 start of strawb field coord = "
                        pos = (y,x)
                        print pos
                        self.strawbFieldStartLocByRowList.append(pos)
                elif (x != 0): #strawb field starts after first col
                    if (self.food[(maxY - y)][x] == True) and (self.food[(maxY - y)][x-1] == False):
                        #print "coord has start of strawb field in it"
                        pos = (y,x)
                        print pos
                        self.strawbFieldStartLocByRowList.append(pos)
                    if (self.food[(maxY - y)][x] == False) and (self.food[(maxY - y)][x-1] == True):
                        #print "coord has end of strawb field in it"
                        pos = (y, (x-1))
                        print pos
                        self.strawbFieldEndLocByRowList.append(pos)
        for y in range(self.height): #num rows
            countPerRow = 0
            self.numStrawbPatchStartsPerRow[y] = []
            for x in range(self.width): #num cols
                pos = (y,x)
                if pos in self.strawbFieldStartLocByRowList:
                    self.numStrawbPatchStartsPerRow[y].append([countPerRow,pos])
                    countPerRow += 1

        for y in range(self.height): #num rows
            countPerRow = 0
            self.numStrawbPatchEndsPerRow[y] = []
            for x in range(self.width): #num cols
                pos = (y,x)
                if pos in self.strawbFieldEndLocByRowList:
                    self.numStrawbPatchEndsPerRow[y].append([countPerRow,pos])
                    countPerRow += 1

        for y in range(self.height):
            print "strawberry patch row " + str(y) + " contained total patches"
            print self.numStrawbPatchStartsPerRow[y]
            print self.numStrawbPatchEndsPerRow[y]

        '''
        for number of strawb patches per row - within the ghDiv calculated
        according to the max num greenhouses - go through each row's number
        of strawb patches, and try to form gh (checking gaps in neg and pos
        directions) for that row - but do it for each strawb patch in row.

        if you have succeeded in forming a gh for all patches in a row
        then you must check the next row - since the patches covered in the
        first row may be different - and some the same - as the second rows
        strawberry patches

        so you should have a count of the number of strawb patches in each
        row - and the start loc of each of those - so you know once you
        move onto check the next row - if the work is already done for that
        row - or you have more work to do in covering a different strawb
        patch for that row, since it may have a different strawb patch than
        the above row.

        also - the strawb gap should fluctuate within a RANGE - since for
        example a gap of 3 - if you check the rows in your ghDiv range -
        and find that the maximum gaps between each of the rows in the ghDiv
        only have a max gap of 2 - should not then check for gap of 3.
        '''

        '''
        so basically - you need to go back and make a value for the number
        of patches in each row along with the start loc for that patch -
        so that at this point here in code - you know whether you have
        more patches to do in this row before moving onto next row -
        and also - if the next rows are all included in this rows' ghs'
        or not

        made the variable - self.numStrawbPatchStartsPerRow dictionary,
        key indexed by row number, with value = num strawb patches in row.
        also made the variable - self.numStrawbPatchEndsPerRow dictionary.
        '''
    def modifyStrawbFieldStartEndLocLists(self):
       maxY = self.height - 1
       maxX = self.width
       strawbPatchGap = 3
       strbGap = 1
       anyStartEndChange = False
       count = 0
       print "starting modify - loop until start/stop positions for gh's do not change"
       while (anyStartEndChange == True) or (strbGap == 1):
           anyStartEndChange,strbGap = self.checkForModify(strawbPatchGap, maxY)
           count = count + 1
           print "loop count = " + str(count)
           print "anyStartEndChange = " + str(anyStartEndChange)

    def checkForModify(self, strawbPatchGap, maxY):
        if (self.maxGHs > (self.height/2)):
            #max num greenhouses > max rows divided by 2
            ghDiv = self.height / 2
            print "max GHs = " + str(self.maxGHs)
            print "self.height / 2 = " + str(self.height / 2)
            print "ghDiv = self.height / 2 = " + str(ghDiv)
        else:
            ghDiv = self.height
            print "ghDiv = maxY = " + str(self.height)
            print "since maxGhs <= (self.height/2), set ghDiv to grid height"
            print "maxGhs = " + str(self.maxGHs)
            
        anyStartEndChange = False
        anyStartEndChangePosDir = False
        anyStartEndChangeNegDir = False
        strbGap = 1
        print "num strawb patch starts and ends per row: patchNum, pos(y,x)"
        for y in range(ghDiv):
            print self.numStrawbPatchStartsPerRow[y]
            print self.numStrawbPatchEndsPerRow[y]
        patchNumEndList = []
        patchNumStartList = []
        numPatchesThisRow = 0
        count = 0
        for y in range(ghDiv):
            currentY = maxY - y
            print "currentY = " + str(currentY)
            patchNumStartList = self.numStrawbPatchStartsPerRow[currentY]
            numPatchesThisRow = len(self.numStrawbPatchStartsPerRow[currentY])
            patchNumEndList = self.numStrawbPatchEndsPerRow[currentY]
            
            print "num patches this row = " + str(numPatchesThisRow)
            for patchNum in range(numPatchesThisRow):

                print "patchNumStartList"
                print patchNumStartList
                currPatchStart = patchNumStartList[patchNum]
                print "currPatchStart"
                print currPatchStart
                pos = currPatchStart[1]

                print "patchNumEndList"
                print patchNumEndList
                currPatchEnd = patchNumEndList[patchNum]
                print "currPatchEnd"
                print currPatchEnd

                '''
                need to change? as follows:
                - add param of where to start in row to check - since
                there are possily multiple patches per row
                - make the greenhouse after you've completed a patch
                within a row, before continuing.
                '''
                
                # if pos is in a previously made greenhouse - skip it

                anyStartEndChangePosDir = self.checkForModifyPosDir(strbGap, strawbPatchGap,maxY,ghDiv,anyStartEndChange,patchNum,pos)
                print "AFTER POS DIR gap check 1 to 3:"
                print "list of start locs of strawbs in rows"
                print self.strawbFieldStartLocByRowList
                print "list of end locs of strawbs in rows"
                print self.strawbFieldEndLocByRowList

                anyStartEndChange = False
                strbGap = -1
                anyStartEndChangeNegDir = self.checkForModifyNegDir(strbGap, (strawbPatchGap * -1), maxY, ghDiv, anyStartEndChange, patchNum, pos)
                anyStartEndChange = anyStartEndChangePosDir or anyStartChangeNegDir
                print "AFTER NEG DIR gap check -1 to -3:"
                print "list of start locs of strawbs in rows"
                print self.strawbFieldStartLocByRowList
                print "list of end locs of strawbs in rows"
                print self.strawbFieldEndLocByRowList

        return anyStartEndChange, strbGap

    def checkForModifyPosDir(self, strbGap, strawbPatchGap, maxY, ghDiv, anyStartEndChange, patchNum, pos):
        print "strbGap = " + str(strbGap)
        print "anyStartEndChange " + str(anyStartEndChange)
        print "checkForModifyPositiveGap: strawbPatchGap = " + str(strawbPatchGap)        
        while (strbGap < strawbPatchGap):
            print "strbGap = " + str(strbGap)
            print "anyStartEndChange " + str(anyStartEndChange)
            print "checkForModifyPosDir: strawbPatchGap = " + str(strawbPatchGap)
            for y in range(ghDiv - 1): # num rows to check
                for x in range(self.width): # num cols are the width
                    currentY = maxY - y
                    xpos = pos[1]
                    if x >= xpos: #start at this strawb patch in row
                        print "current loc this loop"
                        print currentY
                        print x
                        if (x == 0) : #start of row is col 0
                            if (currentY,x) in self.strawbFieldStartLocByRowList: 
                                print "current loc in start loc list"
#if start of row has strawb, do not check prev. row, only next row
#come back to this case later
                        #check next row's start loc (y counts rows here)
                                if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                                    print "checking if this loc is in start loc list"
                                    print currentY - 1
                                    print x + strbGap
                                    if ((currentY > 0) and ((currentY - 1),x + strbGap) in self.strawbFieldStartLocByRowList):
                                        print "removing loc in start loc list"
                                        print currentY - 1
                                        print x + strbGap
                                        self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it 
                                        print "adding loc to start loc list"
                                        print currentY - 1
                                        print x
                                        self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1,x)
                                        if ((currentY <> maxY) and ((currentY + 1),x + strbGap) in self.strawbFieldStartLocByRowList):
                                            print "removing loc in start loc list"
                                            print currentY + 1
                                            print x + strbGap
                                            self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it 
                                            print "adding loc to start loc list"
                                            print currentY + 1
                                            print x
                                            self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                            anyStartEndChange = True
                                            print "anyStartEndChange went True"
                                            displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1,x)

#check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 
                                        if (currentY,x) in self.strawbFieldEndLocByRowList:
                                            print "current loc in end loc list"
                                            if (currentY < maxY) and (x < self.width): #don't go beyond num rows
                                                print "checking if this loc is in end loc list"
                                                print currentY - 1
                                                print x + strbGap
                                            if ((currentY > 0) and (currrentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                                print "removing loc from end list"
                                                print currentY
                                                print x
                                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                                print "adding loc to end list"
                                                print currentY
                                                print x + strbGap
                                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                                anyStartEndChange = True
                                                print "anyStartEndChange went True"
                                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                                            if ((currentY <> maxY) and (currrentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                                print "removing loc from end list"
                                                print currentY
                                                print x
                                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                                print "adding loc to end list"
                                                print currentY
                                                print x + strbGap
                                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                                anyStartEndChange = True
                                                print "anyStartEndChange went True"
                                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

                        elif (x != 0): #strawb field starts after first col
                        #different case since if x==0, can't check col before,
                        #just col after current col
                            print "POS DIR CHECK - x != 0"
                        #check next row's start loc (y counts rows here)
                            if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                                print "POS DIR CHECK - currentY and x in range!"
                                if (currentY,x) in self.strawbFieldStartLocByRowList:
                                    print "POS DIR CHECK - current loc in start loc list!"
                                    if (currentY > 0):
                                        print "POS DIR CHECK - currentY > 0!"
                                        print "checking if this loc is in start loc list"
                                        print currentY - 1
                                        print x + strbGap
                                    if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                        print "POS DIR CHECK - currentY - 1, x + strbGap in start loc list - remove it and put currentY,x there"
                                        print "removing from start loc list"
                                        print currentY - 1
                                        print x
                                        self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                        print "adding to start loc list"
                                        print currentY - 1
                                        print x
                                        self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1, x)
                                    if (currentY <> maxY):
                                        print "POS DIR CHECK - currentY <> maxY"
                                        print "checking if this loc is in start loc list"
                                        print currentY + 1
                                        print x + strbGap
                                    if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                        print "POS DIR CHECK - currentY + 1, x + strbGap in start loc list - remove it - put currentY + 1, x in start loc instead"
                                        print "removing from start loc list"
                                        print currentY + 1
                                        print x
                                        self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                        print "adding to start loc list"
                                        print currentY + 1
                                        print x
                                        self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1, x)


                            #check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 

                                if (currentY,x) in self.strawbFieldEndLocByRowList:
                                    print "current loc in end loc list"
                                    if (currentY > 0):
                                        print "checking if this loc is in end loc list"
                                        print currentY - 1
                                        print x + strbGap
                                    if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                        print "removing loc from end loc list"
                                        print currentY
                                        print x
                                        self.strawbFieldEndLocByRowList.remove((currentY,x))
                                        print "adding loc to end loc list"
                                        print currentY
                                        print x + strbGap
                                        self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                                    if (currentY <> maxY):
                                        print "checking if this loc is in end loc list"
                                        print currentY + 1
                                        print x + strbGap

                                    if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                        print "removing loc from end loc list"
                                        print currentY
                                        print x
                                        self.strawbFieldEndLocByRowList.remove((currentY,x))
                                        print "adding loc to end loc list"
                                        print currentY
                                        print x + strbGap
                                        self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

            print "incrementing strawberry gap from"
            print strbGap
            strbGap = strbGap + 1
            print "to " + str(strbGap)
        print "went thru all strawb patch rows checking start/end locs"
        print "for greenhouses within strabGap range between rows of"
        print str(strawbPatchGap)
        print "returning status of "
        print str(anyStartEndChange)
        print "True means there was a change -should check all ghDiv-rows again"
        print "and loop thru each row again checking start end locs for gh's"
        print "False means there was no change in start / end locs after"
        print "looping through all ghDivrows for various strawb patch gaps betw"
        print "rows and found no modifications of gh start/end locs made"
        return anyStartEndChange,strbGap

    def checkForModifyNegDir(self, strbGap, strawbPatchGap, maxY, ghDiv, anyStartEndChange, patchNum, pos):
        print "strbGap = " + str(strbGap)
        print "anyStartEndChange " + str(anyStartEndChange)
        print "checkForModifyNegativeGap: strawbPatchGap = " + str(strawbPatchGap)
        while (strbGap > strawbPatchGap):
            print "strbGap = " + str(strbGap)
            print "anyStartEndChange " + str(anyStartEndChange)
            print "checkForModifyNegativeGap: strawbPatchGap = " + str(strawbPatchGap)
            for y in range(ghDiv - 1): # num rows are the height
                for x in range(self.width): # num cols are the width
                    currentY = maxY - y
                    xpos = pos[1]
                    if xpos <= x: #start at this strawb patch in row
                        print "current loc this loop"
                        print currentY
                        print x

                        if (x >= (strbGap * -1)): #strawb field starts after first col
                        #different case since if x==0, can't check col before,
                        #just col after current col

                        #check next row's start loc (y counts rows here)
                            if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                                if (currentY,x) in self.strawbFieldStartLocByRowList:
                                    print "current loc in start loc list"
                                    if (currentY > 0):
                                        print "checking if this loc is in start loc list"
                                        print currentY - 1
                                        print x + strbGap
                                    if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                        print "removing from start loc list"
                                        print currentY - 1
                                        print x
                                        self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                        print "adding to start loc list"
                                        print currentY - 1
                                        print x
                                        self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1, x)
                                    if (currentY <> maxY):
                                        print "checking if this loc is in start loc list"
                                        print currentY + 1
                                        print x + strbGap
                                    if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                        print "removing from start loc list"
                                        print currentY + 1
                                        print x
                                        self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                        print "adding to start loc list"
                                        print currentY + 1
                                        print x
                                        self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1, x)


                            #check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 

                                if (currentY,x) in self.strawbFieldEndLocByRowList:
                                    print "current loc in end loc list"
                                    if (currentY > 0):
                                        print "checking if this loc is in end loc list"
                                        print currentY - 1
                                        print x + strbGap
                                    if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                        print "removing loc from end loc list"
                                        print currentY
                                        print x
                                        self.strawbFieldEndLocByRowList.remove((currentY,x))
                                        print "adding loc to end loc list"
                                        print currentY
                                        print x + strbGap
                                        self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                                    if (currentY <> maxY):
                                        print "checking if this loc is in end loc list"
                                        print currentY + 1
                                        print x + strbGap

                                    if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                        print "removing loc from end loc list"
                                        print currentY
                                        print x
                                        self.strawbFieldEndLocByRowList.remove((currentY,x))
                                        print "adding loc to end loc list"
                                        print currentY
                                        print x + strbGap
                                        self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                        anyStartEndChange = True
                                        print "anyStartEndChange went True"
                                        displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

            print "decrementing strawberry gap from"
            print strbGap
            strbGap = strbGap - 1
            print "to " + str(strbGap)
        print "went thru all strawb patch rows checking start/end locs"
        print "for greenhouses within strabGap range between rows of"
        print str(strawbPatchGap)
        print "returning status of "
        print str(anyStartEndChange)
        print "True means there was a change - should check all rows again"
        print "and loop thru each row again checking start end locs for gh's"
        print "False means there was no change in start / end locs after"
        print "looping through all rows for various strawb patch gaps between"
        print "rows and found no modifications of gh start/end locs made"
        return anyStartEndChange,strbGap

"""
    def countStrawbFieldStartEndLocs(self):
        numStartGHLocs = len(self.strawbFieldStartLocByRowList)
        numEndGHLocs = len(self.strawbFieldEndLocByRowList)
        print "numStartGHLocs " + str(numStartGHLocs)
        print "numEndGHLocs " + str(numEndGHLocs)
        return numStartGHLocs

    def findNumGHsNeeded(self):
    #look at strawberry locations within field, max num of greenhouses
    #given in budget, and see how many would be needed, possibly less
    #than the max to save money, depending on your strawberry field
    #The cost of each greenhouse is $10 plus $1 per unit of area covered.
    #The strawberry distribution is not rectangular, but the green houses are.

        #First want to go through list and note start and end loc's
        self.buildStrawbFieldStartEndLocLists()
        print "strawberry field start locations by row list"
        print self.strawbFieldStartLocByRowList
        print "strawberry field end locations by row list"
        print self.strawbFieldEndLocByRowList

        #Then, go through lists of start and end locs of strawberries in rows,
        #and modify the start/end locs by looking at the next and previous
        #rows, so as to best distribute the green houses around them
        #self.modifyStrawbFieldStartEndLocLists()
        #print "strawberry field start locations by row list--MODIFIED"
        #print self.strawbFieldStartLocByRowList
        #print "strawberry field end locations by row list--MODIFIED"
        #print self.strawbFieldEndLocByRowList

        #Now, see how many strawberry fields start and end in same loc
        #That tells you how many greenhouses you need
        #self.numGHsNeeded = self.countStrawbFieldStartEndLocs()

#look at the number of strawberry gaps in the rows and cols already calculated
#look at the location starts of these gaps in the rows and cols and perhaps
#that will tell you the best number of greenhouses to use within max given.

#for each row: look at start and end loc's of strawberry field/patch
#if start of patch is 3 locs or less than row before or after it, include
#in its green house, or if the end of its patch matches with row above it in
# same way (gap betw that patch is 3 or less), and, next row only matches
# (3 or less) with the start of the patch--not the end of the patch--then
# that row's first half matches with one green house, but the end of that
# patch matches with a different green house.

#left off!!
#--modify it!!!
#THEN--modify those lists by gap number in cols of start end in row before
# and after current row
#THEN: (did not do yet!!!)
#- include case where start and end loc's in current row match diff gh's in 
#above and below rows








                #if (self.food[y][x] == True):

                    #self.whichGHLetter(y,x)

    #def whichGHLetter(y,x):
        #s = 0 #strawb count
        #g = 0 #gh count
        
      
    def checkForModifyOldWay(self, strawbPatchGap, maxY):
        returnAnyStartEndChange = False
        anyStartEndChange = False
        anyStartEndChangePos = False
        anyStartEndChangeNeg = False
        strbGap = 1
        anyStartEndChangePos = self.checkForModifyPositiveGap(strbGap,strawbPatchGap,maxY,anyStartEndChange)
        strbGap = -1
        anyStartEndChange = False
        anyStartEndChangeNeg = self.checkForModifyNegativeGap(strbGap,strawbPatchGap * -1,maxY,anyStartEndChange)
        returnAnyStartEndChange = anyStartEndChangePos or anyStartEndChangeNeg
        return returnAnyStartEndChange, strbGap

    def checkForModifyNegativeGap(self, strbGap, strawbPatchGap, maxY, anyStartEndChange):
        print "strbGap = " + str(strbGap)
        print "anyStartEndChange " + str(anyStartEndChange)
        print "checkForModifyNegativeGap: strawbPatchGap = " + str(strawbPatchGap)
        while (strbGap > strawbPatchGap):
            print "strbGap = " + str(strbGap)
            print "anyStartEndChange " + str(anyStartEndChange)
            print "checkForModifyNegativeGap: strawbPatchGap = " + str(strawbPatchGap)
            for y in range(self.height): # num rows are the height
                for x in range(self.width): # num cols are the width
                    currentY = maxY - y
                    print "current loc this loop"
                    print currentY
                    print x

                    if (x >= (strbGap * -1)): #strawb field starts after first col
                        #different case since if x==0, can't check col before,
                        #just col after current col

                        #check next row's start loc (y counts rows here)
                        if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                            if (currentY,x) in self.strawbFieldStartLocByRowList:
                                print "current loc in start loc list"
                                if (currentY > 0):
                                    print "checking if this loc is in start loc list"
                                    print currentY - 1
                                    print x + strbGap
                                if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing from start loc list"
                                    print currentY - 1
                                    print x
                                    self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                    print "adding to start loc list"
                                    print currentY - 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1, x)
                                if (currentY <> maxY):
                                    print "checking if this loc is in start loc list"
                                    print currentY + 1
                                    print x + strbGap
                                if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing from start loc list"
                                    print currentY + 1
                                    print x
                                    self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                    print "adding to start loc list"
                                    print currentY + 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1, x)


                            #check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 

                        if (currentY,x) in self.strawbFieldEndLocByRowList:
                            print "current loc in end loc list"
                            if (currentY > 0):
                                print "checking if this loc is in end loc list"
                                print currentY - 1
                                print x + strbGap
                            if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                print "removing loc from end loc list"
                                print currentY
                                print x
                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                print "adding loc to end loc list"
                                print currentY
                                print x + strbGap
                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                anyStartEndChange = True
                                print "anyStartEndChange went True"
                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                            if (currentY <> maxY):
                                print "checking if this loc is in end loc list"
                                print currentY + 1
                                print x + strbGap

                            if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                print "removing loc from end loc list"
                                print currentY
                                print x
                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                print "adding loc to end loc list"
                                print currentY
                                print x + strbGap
                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                anyStartEndChange = True
                                print "anyStartEndChange went True"
                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

            print "decrementing strawberry gap from"
            print strbGap
            strbGap = strbGap - 1
            print "to " + str(strbGap)
        print "went thru all strawb patch rows checking start/end locs"
        print "for greenhouses within strabGap range between rows of"
        print str(strawbPatchGap)
        print "returning status of "
        print str(anyStartEndChange)
        print "True means there was a change - should check all rows again"
        print "and loop thru each row again checking start end locs for gh's"
        print "False means there was no change in start / end locs after"
        print "looping through all rows for various strawb patch gaps between"
        print "rows and found no modifications of gh start/end locs made"
        return anyStartEndChange,strbGap

    def checkForModifyPositiveGap(self, strbGap, strawbPatchGap, maxY, anyStartEndChange):
        print "strbGap = " + str(strbGap)
        print "anyStartEndChange " + str(anyStartEndChange)
        print "checkForModifyPositiveGap: strawbPatchGap = " + str(strawbPatchGap)        
        while (strbGap < strawbPatchGap):
            print "strbGap = " + str(strbGap)
            print "anyStartEndChange " + str(anyStartEndChange)
            print "checkForModifyPositiveGap: strawbPatchGap = " + str(strawbPatchGap)
            for y in range(self.height): # num rows are the height
                for x in range(self.width): # num cols are the width
                    currentY = maxY - y
                    print "current loc this loop"
                    print currentY
                    print x
                    if (x == 0) : #start of row is col 0
                        if (currentY,x) in self.strawbFieldStartLocByRowList: 
                            print "current loc in start loc list"
#if start of row has strawb, do not check prev. row, only next row
#come back to this case later
                        #check next row's start loc (y counts rows here)
                            if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                                print "checking if this loc is in start loc list"
                                print currentY - 1
                                print x + strbGap
                                if ((currentY > 0) and ((currentY - 1),x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing loc in start loc list"
                                    print currentY - 1
                                    print x + strbGap
                                    self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it 
                                    print "adding loc to start loc list"
                                    print currentY - 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1,x)
                                if ((currentY <> maxY) and ((currentY + 1),x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing loc in start loc list"
                                    print currentY + 1
                                    print x + strbGap
                                    self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it 
                                    print "adding loc to start loc list"
                                    print currentY + 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1,x)

#check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 
                        if (currentY,x) in self.strawbFieldEndLocByRowList:
                            print "current loc in end loc list"
                            if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                                print "checking if this loc is in end loc list"
                                print currentY - 1
                                print x + strbGap
                                if ((currentY > 0) and (currrentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                    print "removing loc from end list"
                                    print currentY
                                    print x
                                    self.strawbFieldEndLocByRowList.remove((currentY,x))
                                    print "adding loc to end list"
                                    print currentY
                                    print x + strbGap
                                    self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                                if ((currentY <> maxY) and (currrentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                    print "removing loc from end list"
                                    print currentY
                                    print x
                                    self.strawbFieldEndLocByRowList.remove((currentY,x))
                                    print "adding loc to end list"
                                    print currentY
                                    print x + strbGap
                                    self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

                    elif (x != 0): #strawb field starts after first col
                        #different case since if x==0, can't check col before,
                        #just col after current col

                        #check next row's start loc (y counts rows here)
                        if (currentY < self.height) and (x < self.width): #don't go beyond num rows
                            if (currentY,x) in self.strawbFieldStartLocByRowList:
                                print "current loc in start loc list"
                                if (currentY > 0):
                                    print "checking if this loc is in start loc list"
                                    print currentY - 1
                                    print x + strbGap
                                if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing from start loc list"
                                    print currentY - 1
                                    print x
                                    self.strawbFieldStartLocByRowList.remove(((currentY - 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                    print "adding to start loc list"
                                    print currentY - 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY - 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY - 1, x + strbGap, currentY - 1, x)
                                if (currentY <> maxY):
                                    print "checking if this loc is in start loc list"
                                    print currentY + 1
                                    print x + strbGap
                                if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldStartLocByRowList):
                                    print "removing from start loc list"
                                    print currentY + 1
                                    print x
                                    self.strawbFieldStartLocByRowList.remove(((currentY + 1),x + strbGap))
                                    #change next col's start loc to match row above it
                                    print "adding to start loc list"
                                    print currentY + 1
                                    print x
                                    self.strawbFieldStartLocByRowList.append(((currentY + 1),x))
                                    anyStartEndChange = True
                                    print "anyStartEndChange went True"
                                    displayStartLoc(currentY,x,currentY + 1, x + strbGap, currentY + 1, x)


                            #check to see if next row's end loc 1,2,3 beyond this row's end loc, and change this row to end the same as that row 

                        if (currentY,x) in self.strawbFieldEndLocByRowList:
                            print "current loc in end loc list"
                            if (currentY > 0):
                                print "checking if this loc is in end loc list"
                                print currentY - 1
                                print x + strbGap
                            if ((currentY > 0) and (currentY - 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                print "removing loc from end loc list"
                                print currentY
                                print x
                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                print "adding loc to end loc list"
                                print currentY
                                print x + strbGap
                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                anyStartEndChange = True
                                print "anyStartEndChange went True"
                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)
                            if (currentY <> maxY):
                                print "checking if this loc is in end loc list"
                                print currentY + 1
                                print x + strbGap

                            if ((currentY <> maxY) and (currentY + 1,x + strbGap) in self.strawbFieldEndLocByRowList):
                                print "removing loc from end loc list"
                                print currentY
                                print x
                                self.strawbFieldEndLocByRowList.remove((currentY,x))
                                print "adding loc to end loc list"
                                print currentY
                                print x + strbGap
                                self.strawbFieldEndLocByRowList.append((currentY,x + strbGap))
                                anyStartEndChange = True
                                print "anyStartEndChange went True"
                                displayEndLoc(currentY,x,currentY,x,currentY, x + strbGap)

            print "incrementing strawberry gap from"
            print strbGap
            strbGap = strbGap + 1
            print "to " + str(strbGap)
        print "went thru all strawb patch rows checking start/end locs"
        print "for greenhouses within strabGap range between rows of"
        print str(strawbPatchGap)
        print "returning status of "
        print str(anyStartEndChange)
        print "True means there was a change - should check all rows again"
        print "and loop thru each row again checking start end locs for gh's"
        print "False means there was no change in start / end locs after"
        print "looping through all rows for various strawb patch gaps between"
        print "rows and found no modifications of gh start/end locs made"
        return anyStartEndChange,strbGap

    def buildStrawbFieldStartEndLocLists(self):
       print "entering buildStrawbFieldStartEndLocLists()"
       maxY = self.height - 1
       print "num rows " + str(self.height)
       print "num cols " + str(self.width)
#self.ghLetList[self.numGHsUsed] = green house letter representation            #self.numGHs = Grid(self.width, self.height, False)    
#above struct holds the gh letters instead of the strawb chars (food has strawbs)     
       for y in range(self.height): # num rows are the height
           for x in range(self.width): # num cols are the width
               if (self.food[maxY - y][x] == True) and (self.food[maxY - y][x-1] == False):
                   self.strawbFieldStartLocByRowList.append(((maxY - y),x))
               #if current y,x has no strawb, but previous y,x-1 does, 
               #then the previous y,x-1 is an end location of strawb field
               #for row y
               if (self.food[maxY - y][x] == False) and (self.food[maxY - y][x-1] == True):
                   self.strawbFieldEndLocByRowList.append(((maxY - y),x-1))

    def countStrawbGaps():
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0): #start of row
                    if (self.food[y][x] == False):
                        self.widthGapList.append((y,x))
                elif (x == 0) and (y == 0): #start of row and col
                    if (self.food[y][x] == False):
                        self.heightGapList.append((y,x))
                elif (x != 0):
                    if (self.food[y][x] == False) and (self.food[y][x-1] == True):
                        self.widthGapList.append((y,x))
                elif (x != 0) and (y != 0):
                    if (self.food[y][x] == False) and (self.food[y-1][x] == True):
                        self.heightGapList.append((y,x))

"""
