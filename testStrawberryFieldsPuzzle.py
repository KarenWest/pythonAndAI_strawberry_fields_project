#This is a test for the strawberry fields puzzle
from strawberryFieldsPuzzle import *
import random

print "Testing the various simulation test cases"
##

random.seed(17) 
average_1=numGHsForStrawberryField(1,1,5,5,1.0,1,0)
print "clock ticks: ",average_1
random.seed(24)
'''
average_2=numGHsForStrawberryField(1,1,10,10,.75,5,0)
print "Should get close to 190 clock ticks: ",average_2,"; Good code got 186.0"
random.seed(88)
average_3=numGHsForStrawberryField(1,1,10,10,.90,5,0)
print "Should get close to 310 clock ticks: ",average_3,"; Good code got 306.2"
random.seed(13)
average_4=numGHsForStrawberryField(1,1,20,20,1.0,5,0)
print 'Should get close to 3322 clock ticks: ',average_4,"; Good code got 3119.2"
random.seed(42)
average_5=numGHsForStrawberryField(3,1,20,20,1.0,5,0)
print 'Should get close to 1105 clock ticks: ',average_5,"; Good code got 1217.0"

random.seed(17)

average_random=numGHsForStrawberryField(1,1,5,5,1.0,1,1)
print "Got from random walk green house worker clock ticks: ",average_random,"; good??"
'''
