#!/usr/bin/python3

# Script: tictactoe.py
# Author: Andrew Smith
# Date: March 2019
# Description: An AI opponent for Tic Tac Toe

###############################
####  SYSTEM REQUIREMENTS  ####
###############################

# Install Python, version 3.6+ to 3.7
# Install PyGame 1.9.6 (Test that it works when installed)
# Can run on Windows and Linux, possibly Mac but not tested on Mac
# Mouse and Keyboard needed for interaction with Tic Tac Toe game

# Include needed libraries
import pygame
import random
import copy
from time import sleep
from pygame.locals import *

#######################################################
########                                       ########
########    GLOBAL VARIABLES / FUNCTIONS       ########
########                                       ########
#######################################################

# Define constants for use in program

#######################
### Screen Settings ###
#######################

# Define Horiz Resolution
HORIZ_RESOLUTION = 1024
# Define Vertical Resolution 
VERT_RESOLUTION = 768

###########################
### Grid Cell Positions ###
###########################

# Grid Cell 1 - Emblem position
GRIDCELL_1X = 350
GRIDCELL_1Y = 250

# Grid Cell 2 - Emblem position
GRIDCELL_2X = 500
GRIDCELL_2Y = 250

# Grid Cell 3 - Emblem position
GRIDCELL_3X = 650
GRIDCELL_3Y = 250

# Grid Cell 4 - Emblem position
GRIDCELL_4X = 350
GRIDCELL_4Y = 350

# Grid Cell 5 - Emblem position
GRIDCELL_5X = 500
GRIDCELL_5Y = 350

# Grid Cell 6 - Emblem position
GRIDCELL_6X = 650
GRIDCELL_6Y = 350

# Grid Cell 7 - Emblem position
GRIDCELL_7X = 350
GRIDCELL_7Y = 450

# Grid Cell 8 - Emblem position
GRIDCELL_8X = 500
GRIDCELL_8Y = 450

# Grid Cell 9 - Emblem position
GRIDCELL_9X = 650
GRIDCELL_9Y = 450

######################
###  Game Emblems  ###
######################

EMBLEM_X = " X "
EMBLEM_0 = " 0 "
EMBLEM_BLANK = " - "

############################
###  ROW ONE CELL RANGES ###
############################

# Cell One Range
CELL1_XFROM = 300
CELL1_XTO = 425
CELL1_YFROM = 200
CELL1_YTO = 296

# Cell Two Range
CELL2_XFROM = 432
CELL2_XTO = 567
CELL2_YFROM = 200
CELL2_YTO = 296

# Cell Three Range
CELL3_XFROM = 572
CELL3_XTO = 696
CELL3_YFROM = 200
CELL3_YTO = 296

############################
###  ROW TWO CELL RANGES ###
############################

# Cell 4 Range 
CELL4_XFROM = 300
CELL4_XTO = 426
CELL4_YFROM = 304
CELL4_YTO = 396

# Cell 5 Range
CELL5_XFROM = 433
CELL5_XTO = 566
CELL5_YFROM = 304
CELL5_YTO = 396

# Cell 6 Range
CELL6_XFROM = 574
CELL6_XTO = 696
CELL6_YFROM = 304
CELL6_YTO = 396

##############################
###  ROW THREE CELL RANGES ###
##############################

# Cell 7 Range
CELL7_XFROM = 300
CELL7_XTO = 426
CELL7_YFROM = 404
CELL7_YTO = 500

# Cell 8 Range
CELL8_XFROM = 433
CELL8_XTO = 566
CELL8_YFROM = 404
CELL8_YTO = 500

# Cell 9 Range
CELL9_XFROM = 574
CELL9_XTO = 696
CELL9_YFROM = 404
CELL9_YTO = 500

# Define row amount for winning
WINNING_TERMINAL_STATE = 3

# Define player identity values
PLAYER_1 = 0
PLAYER_2 = 1

# Stores a collection of players
playerCollection = [ ]

# Initialise PyGame
pygame.init()

# Set screen size / interface
screen = pygame.display.set_mode((HORIZ_RESOLUTION, VERT_RESOLUTION))

# Used to create text to output to PyGame screen
def create_text(text, size, color):
	# Set the font to be used	
	font = pygame.font.SysFont('Comic Sans MS', size)
	
	# Get as image to be shown on screen
	image = font.render(text, True, color)

	return image

#######################################################
########                                       ########
########         CLASS: CellPosition           ########
########                                       ########
#######################################################
####### CellPosition component for a Cell class #######
#######################################################
class CellPosition:
	# Class constructor
	def __init__(self, xPosIn, yPosIn):
		self.xpos_val = xPosIn
		self.ypos_val = yPosIn

	# Method to get X-position of cell	
	def getXPos(self):
		return self.xpos_val

	# Method to get Y-position of cell
	def getYPos(self):
		return self.ypos_val

	# Method to set X-position of cell
	def setXPos(self, xPosIn):
		self.xpos_val = xPosIn

	# Method to set Y-position of cell
	def setYPos(self, yPosIn):
		self.ypos_val = yPosIn


#######################################################
########                                       ########
########             CLASS: Cell               ########
########                                       ########
#######################################################
######   Cell is a main component of the grid  ########
#######################################################
class Cell:
	# Constructor
	def __init__(self, cellIdIn, valueIn, xPosIn, yPosIn):
		self.cellValue = valueIn
		self.cellId = cellIdIn
		self.cellPos = CellPosition(xPosIn, yPosIn)

	# A method to get the value of the cell
	def getCellValue(self):
		return self.cellValue

	# A method to set the value of the cell
	def setCellValue(self, cellValueIn):
		self.cellValue = cellValueIn

	# A method to get the value of cell position x 
	def getCellXPos(self):
		return self.cellPos.getXPos()

	# A method to get the value of cell position y
	def getCellYPos(self):
		return self.cellPos.getYPos()

	# A method to set the value of cell 
	def setCellXPos(self, xPosIn):
		self.cellPos.setXPos(xPosIn)

	# A method to set the value of cell reference row value
	def setCellYPos(self, valueIn):
		self.cellPos.setYPos(yPosIn)


#######################################################
########                                       ########
########         CLASS: GridGameBoard          ########
########                                       ########
#######################################################
########## Main grid platform to hold cells ###########
#######################################################
class GridGameBoard:		
	# Stores a grid of cells for tic tac toe
	theGrid = []

	# Constructor
	def __init__(self):
		self.createGrid()

	# Create the Grid of Cells
	# createGrid
	def createGrid(self):
		# Row 1 of 3 cells
		self.theGrid.append(Cell(1, EMBLEM_BLANK, GRIDCELL_1X, GRIDCELL_1Y))
		self.theGrid.append(Cell(2, EMBLEM_BLANK, GRIDCELL_2X, GRIDCELL_2Y))
		self.theGrid.append(Cell(3, EMBLEM_BLANK, GRIDCELL_3X, GRIDCELL_3Y))

		# Row 2 of 3 cells
		self.theGrid.append(Cell(4, EMBLEM_BLANK, GRIDCELL_4X, GRIDCELL_4Y))
		self.theGrid.append(Cell(5, EMBLEM_BLANK, GRIDCELL_5X, GRIDCELL_5Y))
		self.theGrid.append(Cell(6, EMBLEM_BLANK, GRIDCELL_6X, GRIDCELL_6Y))

		# Row 3 of 3 cells
		self.theGrid.append(Cell(7, EMBLEM_BLANK, GRIDCELL_7X, GRIDCELL_7Y))
		self.theGrid.append(Cell(8, EMBLEM_BLANK, GRIDCELL_8X, GRIDCELL_8Y))
		self.theGrid.append(Cell(9, EMBLEM_BLANK, GRIDCELL_9X, GRIDCELL_9Y))

	# displayGrid
	# Used to display current state of the Grid
	def displayGrid(self):		
		for gridcell in range(len(self.theGrid)): 	
			if self.theGrid[gridcell].getCellValue() == EMBLEM_X:
				screen.blit(xchar, (self.theGrid[gridcell].getCellXPos(), self.theGrid[gridcell].getCellYPos()))

			if self.theGrid[gridcell].getCellValue() == EMBLEM_0:
				screen.blit(ochar, (self.theGrid[gridcell].getCellXPos(), self.theGrid[gridcell].getCellYPos()))	

	# displayGridLines
	# Display Grid Lines on graphics output screen 
	def displayGridLines(self):
		# Horizontal Lines	
		#                          Colour     Start pos    End pos
		pygame.draw.line(screen, (0, 128, 0), (300,200+100), (700, 200+100))
		pygame.draw.line(screen, (0, 128, 0), (300,300+100), (700, 300+100))

		# Vertical Lines
		pygame.draw.line(screen, (0, 128, 0), (430,100+100), (430, 400+100))
		pygame.draw.line(screen, (0, 128, 0), (570,100+100), (570, 400+100))		

	# getCellIndexFromId
	# Used to get cell index from cell index passed in		
	@staticmethod	
	def updateGridCell(cellIndexValueIn, valueIn):
		# A variable to identify if move is success or failure
		moveOutcome = True # Success by default		

		# Check to see if the cell intended is free to select
		if GridGameBoard.theGrid[cellIndexValueIn].getCellValue() == EMBLEM_X or GridGameBoard.theGrid[cellIndexValueIn].getCellValue() == EMBLEM_0:
			moveOutcome = False

		# If the cell is free, then update the game board
		if moveOutcome == True:		
			# Update cell
			GridGameBoard.theGrid[cellIndexValueIn].cellValue = valueIn

		# Return the result of the move		
		return moveOutcome

	# detectHorizCombinationWin
	# Used to detect a horizontal combination win
	@staticmethod
	def detectHorizCombinationWin(playerEmblemIn):
		# Check Horizonal row winnings
		winningRowCombination = [ ] # Stores winning row combination
		
		# Check row 1		
		if GridGameBoard.theGrid[0].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[1].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[2].getCellValue() == playerEmblemIn:
			# Set the winning row combination			
			winningRowCombination.append(0)
			winningRowCombination.append(1)
			winningRowCombination.append(2)

		# Check row 2
		if GridGameBoard.theGrid[3].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[4].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[5].getCellValue() == playerEmblemIn:
			# Set the winning row combination
			winningRowCombination.append(3)
			winningRowCombination.append(4)
			winningRowCombination.append(5)

		# Check row 3
		if GridGameBoard.theGrid[6].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[7].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[8].getCellValue() == playerEmblemIn:
			# Set the winning row combination
			winningRowCombination.append(6)
			winningRowCombination.append(7)
			winningRowCombination.append(8)

		# Return winningRowCombination
		return winningRowCombination

	# detectVertCombinationWin
	# Used to detect a vertical column combination win
	@staticmethod	
	def detectVertCombinationWin(playerEmblemIn):
		# Check vertical column winnings
		winningColCombination = [ ] # Stores winnning index combination

		# Check Column 1
		if GridGameBoard.theGrid[0].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[3].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[6].getCellValue() == playerEmblemIn:
			winningColCombination.append(0)
			winningColCombination.append(3)
			winningColCombination.append(6)

		# Check Column 2
		if GridGameBoard.theGrid[1].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[4].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[7].getCellValue() == playerEmblemIn:
			winningColCombination.append(1)
			winningColCombination.append(4)
			winningColCombination.append(7)

		# Check Column 3
		if GridGameBoard.theGrid[2].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[5].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[8].getCellValue() == playerEmblemIn:
			winningColCombination.append(2)
			winningColCombination.append(5)
			winningColCombination.append(8)

		# Return result
		return winningColCombination

	# detectDiagCombinationWin
	# Used to detect a diagonal win combination
	@staticmethod
	def detectDiagCombinationWin(playerEmblemIn):
		# Check diagonal winnings
		winningDiagCombination = [ ] # Stores the winning combination

		if GridGameBoard.theGrid[0].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[4].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[8].getCellValue() == playerEmblemIn:
			winningDiagCombination.append(0)
			winningDiagCombination.append(4)
			winningDiagCombination.append(8)

		if GridGameBoard.theGrid[2].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[4].getCellValue() == playerEmblemIn and GridGameBoard.theGrid[6].getCellValue() == playerEmblemIn:
			winningDiagCombination.append(2)
			winningDiagCombination.append(4)
			winningDiagCombination.append(6)

		# Return result
		return winningDiagCombination

	@staticmethod
	def detectWinComb(playerEmblemIn):
		hasWon = False # By default there is no win
		winningRowCombination = [] # Stores the index values of the winning row combination

		# Detect for Horizonal row win		
		winningRowCombination = GridGameBoard.detectHorizCombinationWin(playerEmblemIn)

		if len(winningRowCombination) < 1:
			winningRowCombination = GridGameBoard.detectVertCombinationWin(playerEmblemIn)

		if len(winningRowCombination) < 1:
			winningRowCombination = GridGameBoard.detectDiagCombinationWin(playerEmblemIn)

		# Return combination (winning or not)
		return winningRowCombination


	# detectWinningCombination
	# Used to detect a winning combination on the game grid	
	@staticmethod	
	def detectWinningCombination(playerEmblemIn):
		wincomb = GridGameBoard.detectWinComb(playerEmblemIn)

		return wincomb


#######################################################
########                                       ########
########         CLASS: Player                 ########
########                                       ########
#######################################################
######  Player class template for the game  ###########
#######################################################
class Player:
	aiPlayer = False
	moveHistory = [ ]

	# Class constructor
	def __init__(self, idIn, pnameIn, emblemIn):
		self.playerName = pnameIn # Set player name
		self.playerEmblem = emblemIn # Set player emblem
		self.playerWins = 0
		self.playerDraws = 0
		self.playerLosses = 0
		self.id = idIn 

	# Perform player move	
	def performMove(self, gridCellIndexIn):
		GridGameBoard.updateGridCell(gridCellIndexIn, self.playerEmblem)
		# Append to move history
		self.moveHistory.append(gridCellIndexIn)
		# Record as last move
		self.lastMove = gridCellIndexIn

	# Get available moves / positions of gameboard
	def getAvailableMoves(self,gameBoardSource, emblemIn):
		availableMoves = [ ] # Stores a collection of available moves
		indexValue = 0

		while indexValue < 9:
			if gameBoardSource[indexValue].getCellValue() == EMBLEM_BLANK:
				# Add to available moves
				availableMoves.append(indexValue)

			# Increment indexValue
			indexValue = indexValue + 1

		# Return result once gameComplete
		return availableMoves


#######################################################
########                                       ########
########         CLASS: AIPlayer               ########
########                                       ########
#######################################################
######  AI Player class template for the game  ########
#######################################################
class AIPlayer(Player):
	gameBoardState = [ ] # Stores a collection of gameboard states
	enemyValidMoves = [ ] # Collection of enemy valid moves
	firstValidMoves = [ ] # Collection of first valid moves
	scoreCollection = [ ] # Score collection

	firstMove = True # Identify that they are choosing for initial move

	minimaxAI = True # Set as dumb AI player (choses moves @ Random)

	# Class constructor	
	def __init__(self, idIn, pnameIn, emblemIn):
		Player.__init__(self, idIn, pnameIn, emblemIn)
		self.aiPlayer = True
	
	# selectFromCollection
	# A method that selects from a selection of scored outcomes
	def selectFromCollection(self, collectionIn):
		winCollection = [ ] # Stores a collection of winning moves
		looseCollection = [ ] # Stores a collection of loosing movies
		tieCollection = [ ] # Stores a collection of tie / draw scenarios
	
		# Get the collection length
		collectionLength = len(collectionIn)
	
		# Set index counter
		indexCounter = 0
	
		# Loop through and sort the passed in collection
		while indexCounter < collectionLength:
			# Check if win scenario
			if collectionIn[indexCounter][0] == 10:
				winCollection.append(collectionIn[indexCounter])
			
			# Check if loose scenario
			if collectionIn[indexCounter][0] == -10:
				looseCollection.append(collectionIn[indexCounter])
			
			# Check if draw / tie scenario
			if collectionIn[indexCounter][0] == 0:
				tieCollection.append(collectionIn[indexCounter])
			
			# Increment loop index counter
			indexCounter = indexCounter + 1
		
		# Check if there is a win scenario that can be selected
		if len(winCollection) > 0:
			selectedIndexMove = winCollection[0][2]
		
		# Check to see if there is a loose scenario that can be selected
		if len(winCollection) == 0 and len(looseCollection) > 0:
			selectedIndexMove = looseCollection[0][2]
		
		if len(winCollection) == 0 and len(looseCollection) == 0:
			selectedIndexMove = tieCollection[0][2]
		
		# Return the selected move
		return selectedIndexMove

	# detectHorizCombinationWin
	# Detect Horizontal cell combination win
	def detectHorizCombinationWin(self, playerEmblemIn, gboardInstanceIn):
		# Check Horizonal row winnings
		winningRowCombination = [ ] # Stores winning row combination
		
		# Check row 1		
		if gboardInstanceIn[0].getCellValue() == playerEmblemIn and gboardInstanceIn[1].getCellValue() == playerEmblemIn and gboardInstanceIn[2].getCellValue() == playerEmblemIn:
			# Set the winning row combination			
			winningRowCombination.append(0)
			winningRowCombination.append(1)
			winningRowCombination.append(2)

		# Check row 2
		if gboardInstanceIn[3].getCellValue() == playerEmblemIn and gboardInstanceIn[4].getCellValue() == playerEmblemIn and gboardInstanceIn[5].getCellValue() == playerEmblemIn:
			# Set the winning row combination
			winningRowCombination.append(3)
			winningRowCombination.append(4)
			winningRowCombination.append(5)

		# Check row 3
		if gboardInstanceIn[6].getCellValue() == playerEmblemIn and gboardInstanceIn[7].getCellValue() == playerEmblemIn and gboardInstanceIn[8].getCellValue() == playerEmblemIn:
			# Set the winning row combination
			winningRowCombination.append(6)
			winningRowCombination.append(7)
			winningRowCombination.append(8)

		# Return winningRowCombination
		return winningRowCombination

	# detectVertCombinationWin
	# Detect vertical cell combination win
	def detectVertCombinationWin(self, playerEmblemIn, gboardInstanceIn):
		# Check vertical column winnings
		winningColCombination = [ ] # Stores winnning index combination

		# Check Column 1
		if gboardInstanceIn[0].getCellValue() == playerEmblemIn and gboardInstanceIn[3].getCellValue() == playerEmblemIn and gboardInstanceIn[6].getCellValue() == playerEmblemIn:
			winningColCombination.append(0)
			winningColCombination.append(3)
			winningColCombination.append(6)

		# Check Column 2
		if gboardInstanceIn[1].getCellValue() == playerEmblemIn and gboardInstanceIn[4].getCellValue() == playerEmblemIn and gboardInstanceIn[7].getCellValue() == playerEmblemIn:
			winningColCombination.append(1)
			winningColCombination.append(4)
			winningColCombination.append(7)

		# Check Column 3
		if gboardInstanceIn[2].getCellValue() == playerEmblemIn and gboardInstanceIn[5].getCellValue() == playerEmblemIn and gboardInstanceIn[8].getCellValue() == playerEmblemIn:
			winningColCombination.append(2)
			winningColCombination.append(5)
			winningColCombination.append(8)

		# Return result
		return winningColCombination

	# detectDiagCombinationWin
	# Detect diagonal cell combination win
	def detectDiagCombinationWin(self, playerEmblemIn, gboardInstanceIn):
		# Check diagonal winnings
		winningDiagCombination = [ ] # Stores the winning combination

		if gboardInstanceIn[0].getCellValue() == playerEmblemIn and gboardInstanceIn[4].getCellValue() == playerEmblemIn and gboardInstanceIn[8].getCellValue() == playerEmblemIn:
			winningDiagCombination.append(0)
			winningDiagCombination.append(4)
			winningDiagCombination.append(8)

		if gboardInstanceIn[2].getCellValue() == playerEmblemIn and gboardInstanceIn[4].getCellValue() == playerEmblemIn and gboardInstanceIn[6].getCellValue() == playerEmblemIn:
			winningDiagCombination.append(2)
			winningDiagCombination.append(4)
			winningDiagCombination.append(6)

		# Return result
		return winningDiagCombination

	
	# detectWinComb
	# Detect winning combination
	def detectWinComb(self, emblemIn, gboardInstanceIn):
		hasWon = False # By default there is no win
		winningRowCombination = [] # Stores the index values of the winning row combination

		# Detect for Horizonal row win		
		winningRowCombination = self.detectHorizCombinationWin(emblemIn, gboardInstanceIn)

		# Detect for vertical win
		if len(winningRowCombination) < 1:
			winningRowCombination = self.detectVertCombinationWin(emblemIn, gboardInstanceIn)

		# Detect for diagonal win
		if len(winningRowCombination) < 1:
			winningRowCombination = self.detectDiagCombinationWin(emblemIn, gboardInstanceIn)

		# Return combination (winning or not)
		return winningRowCombination

	# scoreInstance
	# Used to score a gameboard instance (-10, +10, 0)
	def scoreInstance(self, gameBoardInstanceIn, indexValueIn):
		looseOutcome = False
		winOutcome = False
		instanceScore = 0 # Stores instance score
		
		# Copy the instance that has been passed in
		gboardInstance = copy.deepcopy(gameBoardInstanceIn)

		# If emblem changed to opponent emblem, does it result in a win?
		if self.playerEmblem == EMBLEM_X:
			# Update gameboard instance with emblem
			# gameBoardInstanceIn.updateGridCell(indexValueIn, EMBLEM_0)
			gboardInstance[indexValueIn].setCellValue(EMBLEM_0)

			# Check to see if opponent has won the game
			winningComb1 = self.detectWinComb(EMBLEM_0, gboardInstance)
			
			# Check to see if a win
			if len(winningComb1) == WINNING_TERMINAL_STATE:
				# instanceScore = -10 
				looseOutcome = True

			if len(winningComb1) < WINNING_TERMINAL_STATE:
				instanceScore = 0

			# Check to see if we win if we were there
			# gameBoardInstanceIn.updateGridCell(indexValueIn, EMBLEM_X)
			gboardInstance[indexValueIn].setCellValue(EMBLEM_X)

			# Check for winning combination of gameboard instance
			winningComb2 = self.detectWinComb(EMBLEM_X, gboardInstance)

			# Detect win or draw
			if len(winningComb2) == WINNING_TERMINAL_STATE:
				# instanceScore = 10
				winOutcome = True

			if len(winningComb2) < WINNING_TERMINAL_STATE:
				instanceScore = 0
				
		# Decide on the return result
		if winOutcome == True:
			instanceScore = 10
			
		if winOutcome == False and looseOutcome == True:
			instanceScore = -10
			
		if winOutcome == False and looseOutcome == False:
			instanceScore = 0		

		# Return instance score
		return instanceScore

	# getMiniMaxAIMove (MAIN AI ALGORITHM)
	# MiniMax AI implementation
	def getMiniMaxAIMove(self, validMovesIn):
		indexCounter = 0 # Index counter for loop
		gameBoardInstance = [ ] # Collection of gameboard instances
		chosenMove = -1 # No move selected by default
		validMoveCollection = [ ] # Stores collection of valid moves

		if self.firstMove == False:

			if len(validMovesIn) > 0:
				indexCounter = 0

				while indexCounter < len(validMovesIn):

					# Get a gameboard copy
					gboardInstance = copy.deepcopy(GridGameBoard.theGrid)

					# Implement a valid move onto the gameboard instance
					cellIndex = validMovesIn[indexCounter]			
				
					# Mark AI Player emblem in 
					gboardInstance[cellIndex].setCellValue(self.playerEmblem)
					
					# Score GameBoard instance
					instanceScore = self.scoreInstance(gboardInstance, cellIndex)
					
					# Add to score collection
					self.scoreCollection.append([instanceScore, indexCounter, cellIndex])
					
					# DEBUG OUTPUT CODE
					
					# Output GameBoard instance
					self.debugOutputBoardInstances(gboardInstance)
					
					# Output Score for gameboard instance
					print("\nScore: " + str(instanceScore))
				
					# Add current instance of GridGameBoard.theGrid
					gameBoardInstance.append(gboardInstance)

					# Increment index counter
					indexCounter = indexCounter + 1
					
				# Debug output to see how has worked so far
				indexCounter = 0 # Reset counter
				
				# Choose the move based on scored game board outcomes
				chosenMove = self.selectFromCollection(self.scoreCollection)
				
				# Reset the score collection
				self.scoreCollection = [ ]
					
				return chosenMove

		if self.firstMove == True:			
			# Check if player chose cell index 0 first
			if GridGameBoard.theGrid[0].getCellValue() ==  EMBLEM_0:
				# Mirror opponents move
				chosenMove = 4
				# Identify that first move has been taken
				self.firstMove = False # Identify first move has been taken

			# Check if human player chose cell index 1 first
			if GridGameBoard.theGrid[1].getCellValue() == EMBLEM_0:
				# Mirror opponents move for first move
				chosenMove = 7
				# Identify that first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 2 first
			if GridGameBoard.theGrid[2].getCellValue() == EMBLEM_0:
				# Mirror opponents move
				chosenMove = 4
				# Identify that first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 3 first
			if GridGameBoard.theGrid[3].getCellValue() == EMBLEM_0:
				# Choose first valid move @ random
				chosenMove = 5 # Choose opposite move
				# Identify first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 4 first
			if GridGameBoard.theGrid[4].getCellValue() == EMBLEM_0:
				self.firstValidMoves.append(0)				
				self.firstValidMoves.append(2)				
				self.firstValidMoves.append(6)
				self.firstValidMoves.append(8)

				# Choose first move @ random
				chosenMove = random.choice(self.firstValidMoves)
				# Identify that first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 5 first
			if GridGameBoard.theGrid[5].getCellValue() == EMBLEM_0:
				# Choose first move @ random
				chosenMove = 3
				# Identify first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 6 first
			if GridGameBoard.theGrid[6].getCellValue() == EMBLEM_0:
				# Select opponent mirror 
				chosenMove = 4
				# Identify first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 7 first
			if GridGameBoard.theGrid[7].getCellValue() == EMBLEM_0:
				# Choose opponent mirror move
				chosenMove = 1
				# Identify that first move has been taken
				self.firstMove = False

			# Check if human player chose cell index 8 first
			if GridGameBoard.theGrid[8].getCellValue() == EMBLEM_0:
				# Choose opponent mirror move
				chosenMove = 4
				# Identify that first move has been taken
				self.firstMove = False		

		# Return the chosen move
		return chosenMove

	# debugOutputBoardInstances
	# Debug output method for outputting gameboard instances
	def debugOutputBoardInstances(self, boardInstanceIn):
		# Get the gameboard instance to output
		selectedInstance = boardInstanceIn

		print("\n\n")

		# Output cell 0
		print(selectedInstance[0].getCellValue() + " " + selectedInstance[1].getCellValue() + " " + selectedInstance[2].getCellValue())
		print(selectedInstance[3].getCellValue() + " " + selectedInstance[4].getCellValue() + " " + selectedInstance[5].getCellValue())
		print(selectedInstance[6].getCellValue() + " " + selectedInstance[7].getCellValue() + " " + selectedInstance[8].getCellValue())

	# decideMove
	# Decide move of AI player (Possible recursive method)
	def decideMove(self):
		validMoves = [ ] # Stores valid moves
		moveSelected = -1 # By default no move has been selected

		# Dumb AI Player - Get valid move @ Random
		if self.minimaxAI == False:
			# Get available AI Player moves from GameBoard
			validMoves = self.getAvailableMoves(GridGameBoard.theGrid, " X ")

			# Select at random a valid move
			moveSelected = self.getMoveAtRandom(validMoves)

		# MiniMax AI Player - Analyse gameboard outcomes
		if self.minimaxAI == True:
			# Get available AI Player moves from GameBoard
			validMoves = self.getAvailableMoves(GridGameBoard.theGrid, " X ")

			# Get AI calculated move
			moveSelected = self.getMiniMaxAIMove(validMoves)

		# Return the move that has been selected
		return moveSelected

	# getMoveAtRandom
	# Select a valid move at random	
	def getMoveAtRandom(self, validMovesIn):
		moveSelected = -1 # No move selected by default

		# Check if there is a selection to choose from
		if len(validMovesIn) > 1:
			moveSelected = random.choice(validMovesIn)

		# Check if there is only one to select from
		if len(validMovesIn) == 1:
			moveSelected = validMovesIn[0]

		# Check if there is none to select from
		if len(validMovesIn) == 0:
			moveSelected = -1; 

		# Return the selected move		
		return moveSelected

	# performAIMove
	# Perform move of AI player
	def performAIMove(self):
		moveDecided = self.decideMove()

		if moveDecided != -1:
			GridGameBoard.updateGridCell(moveDecided, self.playerEmblem)
			return True

		if moveDecided == -1:
			return False	


#######################################################
########                                       ########
########               GAME SETUP              ########
########                                       ########
#######################################################

# Create and Setup Gameboard
gameBoard = GridGameBoard()

# Setup human player
humanPlayer = Player(1, "Andrew", EMBLEM_0)

# Setup AI Player
aiPlayer = AIPlayer(2, "Computer", EMBLEM_X)

# Add players to playerCollection
playerCollection.append(humanPlayer)
playerCollection.append(aiPlayer)

pygame.display.set_caption('TIC TAC TOE')
clock = pygame.time.Clock()

gameComplete = False # Flag to identify when main game loop is to stop

programEnd = False # A flag to identify when the program is to end

text = create_text("TIC TAC TOE", 72, (0, 128, 0))
xchar = create_text("X", 32, (0, 128, 0)) # Create X Character
ochar = create_text("O", 32, (0, 128, 0)) # Create 0 Character
nchar = create_text(" ", 32, (0, 0, 0)) # Create no character (blank)

# Human Player Text
humanText = create_text("HUMAN PLAYER: 0", 18, (0, 128, 0))

# AI Player Text
aiText = create_text("AI PLAYER: X", 18, (0, 128, 0))

# Black coloured screen	
screen.fill((0, 0, 0))	

# Display Tic Tac Toe gridlines
gameBoard.displayGridLines()

# Randomly select a player to go first
turn_indicator = PLAYER_1

# A function to detect game end state
# Returns -1 (No complete state)
# Returns 0 (Draw state)
# Returns 1 (PLAYER_1) win
# Returns 2 (PLAYER_2) win
def detectGameEndState():
	# Variable to return to end result
	gameState = -1 # By default the game has not ended

	# Detect if PLAYER_1 has won
	winCombination = GridGameBoard.detectWinningCombination(playerCollection[PLAYER_1].playerEmblem)

	# Check to see if combination win
	if len(winCombination) == WINNING_TERMINAL_STATE:
		gameState = PLAYER_1 # Identify that player one wins

	# Check to see if PLAYER_2 has won if game state has not changed from the default
	if gameState == -1:
		# Detect if PLAYER_2 has won
		winCombination = GridGameBoard.detectWinningCombination(playerCollection[PLAYER_2].playerEmblem)

		if len(winCombination) == WINNING_TERMINAL_STATE:
			gameState = PLAYER_2 # Identify that player two wins

	if gameState != PLAYER_1 and gameState != PLAYER_2:
		blank_counter = 0
		icounter = 0
		tgrid = copy.deepcopy(GridGameBoard.theGrid)
		while icounter < len(tgrid):
			if tgrid[icounter].getCellValue() == EMBLEM_BLANK:
				blank_counter = blank_counter + 1
			icounter = icounter + 1
		
		if blank_counter == 0:
			gameState = 2

	# Return the current game state
	return gameState

#######################################################
########                                       ########
########         MAIN GAMING LOOP              ########
########                                       ########
#######################################################

while not programEnd:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			programEnd = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			programEnd = True
		if event.type == MOUSEBUTTONDOWN:
			#print event.button
			# print pygame.mouse.get_pos()	
			mpos = pygame.mouse.get_pos()
			xval = mpos[0]
			yval = mpos[1]

			# Identify turn and if human player go or not
			if turn_indicator == PLAYER_1 and playerCollection[turn_indicator].aiPlayer == False:

				# (FIRST ROW SELECTION)
				
				# Detect Cell 1 select
				if xval >= CELL1_XFROM and xval <= CELL1_XTO and yval >= CELL1_YFROM and yval <= CELL1_YTO:
					playerCollection[turn_indicator].performMove(0)
					turn_indicator = PLAYER_2 # Change player

				# Detect Cell 2 select
				if xval >= CELL2_XFROM and xval <= CELL2_XTO and yval >= CELL2_YFROM and yval <= CELL2_YTO:
					playerCollection[turn_indicator].performMove(1)
					turn_indicator = PLAYER_2

				# Detect Cell 3 select
				if xval >= CELL3_XFROM and xval <= CELL3_XTO and yval >= CELL3_YFROM and yval <= CELL3_YTO:
					playerCollection[turn_indicator].performMove(2)
					turn_indicator = PLAYER_2

				# (SECOND ROW SELECTION)

				# Detect Cell 4 select
				if xval >= CELL4_XFROM and xval <= CELL4_XTO and yval >= CELL4_YFROM and yval <= CELL4_YTO:
					playerCollection[turn_indicator].performMove(3)
					turn_indicator = PLAYER_2

				# Detect Cell 5 select
				if xval >= CELL5_XFROM and xval <= CELL5_XTO and yval >= CELL5_YFROM and yval <= CELL5_YTO:
					playerCollection[turn_indicator].performMove(4)
					turn_indicator = PLAYER_2

				# Detect Cell 6 select
				if xval >= CELL6_XFROM and xval <= CELL6_XTO and yval >= CELL6_YFROM and yval <= CELL6_YTO:
					playerCollection[turn_indicator].performMove(5)
					turn_indicator = PLAYER_2

				# (THIRD ROW SELECTION)

				# Detect Cell 7 select
				if xval >= CELL7_XFROM and xval <= CELL7_XTO and yval >= CELL7_YFROM and yval <= CELL7_YTO:
					playerCollection[turn_indicator].performMove(6)
					turn_indicator = PLAYER_2

				# Detect Cell 8 select
				if xval >= CELL8_XFROM and xval <= CELL8_XTO and yval >= CELL8_YFROM and yval <= CELL8_YTO:
					playerCollection[turn_indicator].performMove(7)
					turn_indicator = PLAYER_2

				# Detect Cell 9 select
				if xval >= CELL9_XFROM and xval <= CELL9_XTO and yval >= CELL9_YFROM and yval <= CELL9_YTO:
					playerCollection[turn_indicator].performMove(8)
					turn_indicator = PLAYER_2
				
				gameBoard.displayGrid()
				
				# Check for terminal game state
				gState = detectGameEndState()

				if gState != -1:
					turn_indicator = PLAYER_2

				# If ending in a winning / terminal state, output who has won the game
				if gState == PLAYER_1:
					print("PLAYER ONE WINS!")
					gameComplete = True

				if gState == PLAYER_2:
					print("PLAYER TWO WINS!")
					gameComplete = True

				if gState == 2:
					print("DRAW!!")
					gameComplete = True

	# Change turn indicator
	if turn_indicator == PLAYER_2 and playerCollection[turn_indicator].aiPlayer == True:
		# Check to see if a terminal state has been reached		
		gState = detectGameEndState()

		# Only continue if there is no win
		if gState == -1:
			moveResult = playerCollection[turn_indicator].performAIMove()
			gameBoard.displayGrid()
			
			# Check to see if move ends game or wins, etc...
			gState = detectGameEndState()
			
			if gState == -1:
				turn_indicator = PLAYER_1
				
			if gState == PLAYER_2:
				print("AI PLAYER WINS")
				gameComplete = True
				
			if gState == 2:
				print("DRAW!")
				gameComplete = True

	# Output game title	
	screen.blit(text,((1024/4),0))
	screen.blit(humanText, (20, 100))
	screen.blit(aiText, (20, 140))
	# gameBoard.displayGrid()

	pygame.display.flip()
	clock.tick(60)
	
	# If the game is complete reset the game so
	# play can continue
	if gameComplete == True:
		gameComplete = False
		
		GridGameBoard.theGrid = [ ]
		gameBoard.createGrid()
		
		screen.fill((0,0,0))
		
		sleep(2)
		
		gameBoard.displayGridLines()
		gameBoard.displayGrid()
		turn_indicator = PLAYER_1
		
		# Set AI player back to normal
		playerCollection[PLAYER_2].firstMove = True
		
		pygame.display.flip()
		clock.tick(60)
	
print("End of Program")
sleep(2)
pygame.quit()