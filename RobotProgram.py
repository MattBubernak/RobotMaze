# Program Name: RobotProgram.py
# Author: Matt Bubernak
# Date: 10/6/2015
# Description: Provided an input file containing a grid, defined by the following 
#              character set: [.,R,O,T] , the program will tell you if there is a 
#              connection between R and T through the grid, that doesn't go through
#              an O. Will output 'Yes' or 'No'.
# Example 'Yes' Input File: 
# 					  ...
#                     RO.
#                     ..T
# Example 'No' Input File: 
# 					  ...
#                     ROO
#                     .OT
# Usage: (cmd to run python may vary...) py RobotProgram.py [input.txt]

import os.path
import sys

# Used to as an element of a grid, acts as a tuple of a character and boolean 
# for whether it has been visited. 
class GridElem:
	def __init__(self,val):
		self.value = val
		self.visited = False

# Used to store the input file, translated to a 2D array. 
class Grid: 
	def __init__(self,inputText):
		# We can store a 2D array as a dictionary.
		self.gridArr = {} 
		# We will find this when we load a grid.
		self.robotX = -1   
		self.robotY = -1
		self.targetX = -1   
		self.targetY = -1
		self.invalidChars = False  
		# Used for incramenting
		i = 0
		j = 0

		# Loop through every line. 
		for line in inputText: 
			# Split line into characters, and add them to the gridArr
			for char in list(line.rstrip()):

				# Add the gridElem to the grid, if it's a valid character
				if (char.lower() in ['r','t','.','o']):
					self.gridArr[i,j] = (GridElem(char.lower()))
				# Mark that we have found an invalid character otherwise. 
				else: 
					self.invalidChars = True

				# Document the location of our robot and target
				if (char.lower() == 'r'):
					self.robotX = j
					self.robotY = i
				elif (char.lower() == 't'):
					self.targetX = j
					self.targetY = i

				# Incrament j(coorelating to the width)
				j+=1

			# Apply appropriate modifications to i/j
			i += 1
			j = 0

	# Returns whether the grid as a whole is valid. The only concerns we have
	# are that it contains a robot and a target, and no invalid characters
	def validGrid(self):
		if ((self.robotX != -1) and (self.robotY != -1) and (self.targetX != -1)   
		and (self.targetY != -1) and (self.invalidChars == False)):
			return True
		else: 
			return False  

	# Returns whether a given index combination is valid. 
	def validLocation(self,x,y):
		if (y,x) in self.gridArr:
			return True
		return False

	# Marks a location as visited. 
	def visitLocation(self,x,y):
		self.gridArr[y,x].visited = True

	# Gets the value at a location in the array. If it's an invalid index
	# returns None 
	def get(self,x,y):
		if (y,x) in self.gridArr:
			return self.gridArr[y,x]
		else: 
			return None 

class Solver: 
	def __init__(self):
		pass
	# Recursive helper function for the solveGrid method. 
	def solveRecurse(self,grid,x,y):
		# Verify it's a valid location
		if (grid.validLocation(x,y) == False):
			return False

		# If we have already been here, or it's not valid, or it's an obstacle
		elif ((grid.get(x,y).value == 'o') or (grid.get(x,y).visited == True)):
			return False

		# If it's the target, return true. 
		elif (grid.get(x,y).value == 't'):
			return True

		# Else try all adjacent locations. 
		else:
			grid.visitLocation(x,y)
			solveDown = self.solveRecurse(grid,x,y+1)
			solveUp = self.solveRecurse(grid,x,y-1)
			solveLeft = self.solveRecurse(grid,x-1,y)
			solveRight = self.solveRecurse(grid,x+1,y)
			return (solveUp or solveDown or solveLeft or solveRight)

	# Returns True/False depending on if there is a path between a robot and target
	# If the grid is invalid, doesn't do this check and outputs to user. 
	def solveGrid(self,grid):
		if (grid.validGrid() != True): 
			print("Grid is invalid.")
			return False
		else:
			return self.solveRecurse(grid,grid.robotX,grid.robotY) 

def main(): 
	# The 'solver' that we will load with a grid, and asked to solve it. 
	solver = Solver() 

	# Verify the user provided correct format of input. 
	if (len(sys.argv) < 2 or len(sys.argv) > 2):
		print("Usage: ./RobotProgram.py [input.txt]")
		return

	# If the correct input format was provided
	else: 
		inputPath = sys.argv[1]
		# If the file exists pass the input to the solver.
		if (os.path.exists(inputPath)):
			fileObj = open(inputPath,'r')
			lines = fileObj.readlines()
			result = solver.solveGrid(Grid(lines))
			if (result == True): 
				print("yes")
			else: 
				print("no")

		# Else, inform user of invalid input and return
		else: 
			print("File: " + inputPath + " doesn't exist.")

		return

# Call the main logic of this program. 
main()