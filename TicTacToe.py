#Global constants and variables
WIN_INDICES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
TOKEN_XREF = [[0, 3, 6], [0,4], [0, 5, 7], [1,3], [1, 4, 6, 7], [1, 5], [2, 3, 7], [2, 4], [2, 5, 6]]

# Experiment Generator:
class ExperimentGenerator:
	# Generate first board
	def generate_experiment(self):
		board = [0] * 9
		return board
		
	# Print board
	# Player 1 = X
	# Player 2 = O
	# Blank spaces 0 = _
	def print_board(self, board):
		print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[0:3]]))
		print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[3:6]]))
		print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[6:9]]))
		print()


	# Read weights from file
	def read_weights(self):
		try:
			weights = []
			file = open("weights.txt", "r")
			for line in file:
				weights.append(float(line.strip()))
			file.close()
		except FileNotFoundError:
			weights = [0.01] * 8
		else:
			if len(weights) == 0:
				weights = [0.01] * 8
		
		return weights
				
		
# Performance System:
class PerformanceSystem:
	player_nbr = 0
	game_history = []
	
	# Constructor
	def __init__(self, player_nbr):
		self.player_nbr = player_nbr
		self.game_history = []

	# Convert board to feature set
	def get_featureset(cls, board):
		#initialize x0 = 1
		featureset = [1]
		
		#x1 = number of turns
		featureset.append(sum(1 for elem in board if elem == 1))

		#x2 = number of open lines with 1 token - player 1
		#x3 = number of open lines with 1 token - player 2
		#x4 = number of open lines with 0 tokens
		#x5 = number of open lines with 2 tokens - player 1
		#x6 = number of open lines with 2 tokens - player 2
		#x7 = number of lines with 3 tokens - player 1
		#x8 = number of lines with 3 tokens - player 2
		x2, x3, x4, x5, x6, x7, x8 = 0, 0, 0, 0, 0, 0, 0
		p1_lines, p2_lines = [], []
		for row in WIN_INDICES:
			board_slice = [board[idx] for idx in row if board[idx] > 0]
			#print("inside get features")
			#print(board_slice)
			#print(len(set(board_slice)))
			if len(set(board_slice)) == 1:
				if board_slice[0] == 1:
					x2 += 1
					p1_lines.append(1)
					p2_lines.append(0)
					if len(board_slice) > 2:
						x7 += 1
					elif len(board_slice) > 1:
						x5 += 1
				elif board_slice[0] == 2:
					x3 += 1
					p2_lines.append(1)
					p1_lines.append(0)
					if len(board_slice) > 2:
						x8 += 1
					elif len(board_slice) > 1:
						x6 += 1
				else:
					x4 += 1
					p2_lines.append(1)
					p1_lines.append(1)
			else :
				p1_lines.append(0)
				p2_lines.append(0)
		#print("attrib 2-8: " + str(x2) + " " + str(x3) + " " + str(x4) + " " + str(x5) + " " + str(x6) + " " + str(x7) + " " + str(x8))
		
		#x9 = number of points with 2 or more open lines - player 1
		#x10 = number of points with 2 or more open lines - player 2
		x9, x10 = 0, 0
		import operator
		#print(p1_lines)
		#print(p2_lines)
		if p1_lines.count(1) or p2_lines.count(1):
			for row in TOKEN_XREF:
				if p1_lines.count(1):
					if operator.itemgetter(*row)(p1_lines).count(1) > 1:
						x9 += 1
				if p2_lines.count(1):
					if operator.itemgetter(*row)(p2_lines).count(1) > 1:
						x10 += 1
		
		#Construct and return featureset
		featureset.extend([x2, x3, x4, x5, x6, x7, x8, x9, x10])
		return featureset

		
	# Calculate board score
	def board_score_estimate(cls, attributes, weights):
		#print("Board attributes: ")
		#print(board)
		#print(attributes)
		#print(sum([w*a for w, a in zip(weights, attributes)]))
		
		#Compute and return rating
		return sum([w*a for w, a in zip(weights, attributes)])
		
		
	# Pick and play best move
	def play_move(self, board, weights):
		#max_score = -100
		
		opp_player_nbr = lambda: 2 if self.player_nbr == 1 else 2

		#Count number of blank spaces on board
		open_spaces = sum(1 for elem in board if not elem)
		#print("Open spaces=" + str(open_spaces))
		
		#Add board to game history
		self.game_history.append(' '.join(map(str,board)))
		
		#For each space where next token can be added
		#Identify moves for opponent
		#For each space and opponent move. calculate board score
		#Keep track of board with max score and select it as my move
		if open_spaces > 1:
			for idx, elem in enumerate(board):
				#Identify open spaces on board
				if not elem:
					#Copy board to temp copy
					next_board = list(board)
					#Mark my move
					next_board[idx] = self.player_nbr
					#Iterate thru possible opponent moves
					for nb_idx, nb_elem in enumerate(next_board):
						if not nb_elem:
							#Mark opponent move
							next_board[nb_idx] = opp_player_nbr()
							#print_board(next_board)
							#Convert board to featureset
							attributes = self.get_featureset(next_board)
							#Calculate board score
							score = self.board_score_estimate(attributes, weights)
							#Reset opponent move
							next_board[nb_idx] = 0
							#Check max score
							if "max_score" in locals():
								if score > max_score:
									max_score = score
									move = idx
									#print("Inside max score:" + str(move))
							else:
								max_score = score
								move = idx
								#print("Inside max score:" + str(move))
			
			#Select move with highest board score
			if move >= 0:
				board[move] = self.player_nbr
				#print("selected move: " + str(move))
		
		#If only one space is available, select it for next move
		elif open_spaces == 1:
			board[board.index(0)] = self.player_nbr
		
		return board
		
		
	# Check board for victory condition
	def evaluate_win(self, board):
		victor = 0
		for row in WIN_INDICES:
			board_slice = [board[idx] for idx in row]
			if len(set(board_slice)) == 1:
				victor = set(board_slice).pop()
				break
		if not victor and not board.count(0):
			victor = 3
		return victor

	# Play human move	
	def human_move(self, board, player_nbr):
		#Ask human for move
		human_move = input("Enter your move..")
		
		#Apply human move
		board[int(human_move)]= player_nbr
		#print_board(board)
		return board

	
# Critic
class Critic:
	# Given game history, generates training examples	
	def generate_train_data(self, victor, game_history, weights):
		#Set final score based on victor
		if victor == 1:
			final_score = 100
		elif victor == 2:
			final_score = -100
		else:
			final_score = 0
		
		training_data = []		
		#Assign final_score for final board position
		#Assign score estimate of successor board for other board positions
		for idx, board in enumerate(reversed(game_history)):
			if idx == 0:
				score = final_score
			else:
				#print(next_board)
				#Convert board to featureset
				attributes = PerformanceSystem(1).get_featureset(next_board)
				score = PerformanceSystem(1).board_score_estimate(attributes, weights)
			#Assign current board as successor board for next board
			next_board = list(map(int, board.split(' ')))
			#Append training data
			training_data.append([board, score])
			#print(board)
			#print(score)
		
		return training_data
	
	
# Generalizer:
class Generalizer:
	# Train the algorithm using training examples and update the weights
	def train_algo(self, train_data, weights):
		train_rate = 0.1
		for example in train_data:
			#Unpack board and rating
			board = list(map(int, example[0].split(' ')))
			rating = example[1]
			#print(board)
			#print(rating)
			
			
			#Calculate board score using current weights
			attributes = PerformanceSystem(1).get_featureset(board)
			score = PerformanceSystem(1).board_score_estimate(attributes, weights)
			#print("Training::" + str(rating) + " " + str(score))
			#print(attributes)
			
			#Update weights
			revised_weights = []
			for idx, weight in enumerate(weights):
				revised_weights.append(weight + train_rate * (rating - score) * attributes[idx])
				#print("weight loop")
				#print(weight)
				#print(rating - score)
				#print(attributes[idx])
			#print(revised_weights)
			weights = revised_weights
		
		return revised_weights
		
		
	# Save training data to CSV dump
	def save_train_data(self, train_data):
		import csv
		with open("data.csv", "a", newline='') as f:
			writer = csv.writer(f)
			for instance in train_data:
				#writer.writerow(' '.join(map(str,instance)))
				writer.writerow(instance)
				

	# Update new weights in file
	def update_weights(self, new_weights):
		#Delete archive file
		import os
		try:
			os.remove("weights_archive.txt")
		except FileNotFoundError:
			pass
		
		#Rename existing file to archive
		try:
			os.rename("weights.txt", "weights_archive.txt")
		except FileNotFoundError:
			pass
		
		#Write to weights file
		file = open("weights.txt", "w")
		for weight in new_weights:
			file.write(str(weight) + '\n')
		file.close()
	
	
# Main function
def main():
	import sys
	# Make a list of command line arguments, omitting the [0] element
	# which is the script itself.
	args = sys.argv[1:]
	if not args:
		default_play = True
	elif args[0] == '--human':
		default_play = False
	else:
		print("usage: [--human] for human vs ai")
		sys.exit(1)

	if default_play:
		print('Training the AI...')
		#Play AI vs AI for 2000 games
		for i in range(0,2000):
			#Generate experiment
			experiment = ExperimentGenerator()
			board = experiment.generate_experiment()
			#print(board)
			#experiment.print_board(board)
			
			#Get initial weights
			weights = experiment.read_weights()
			#print("Initial weights:")
			#print(weights)
			
			#Initialize players
			player1 = PerformanceSystem(1)
			player2 = PerformanceSystem(2)
				
			#Play game till it is either won or tied
			victor = 0
			while not victor and board.count(0) > 0:
				#Player 1 move
				board = player1.play_move(board, weights)
				#experiment.print_board(board)
				victor = player1.evaluate_win(board)
			
				#Player 2 move if victor is not decided
				if not victor and board.count(0) > 0:
					board = player2.play_move(board, weights)
					#experiment.print_board(board)
					victor = player2.evaluate_win(board)
				
			game_history = player1.game_history
			#print(game_history)
			'''
			if victor == 1:
				print("Player 1 wins!")
			elif victor == 2:
				print("Player 2 wins!")
			else:
				print("It is a tie!")
			'''

			#Convert game history to training examples
			critic = Critic()
			train_data = critic.generate_train_data(victor, game_history, weights)
			#print(train_data)
			
			#Append training data to CSV dump
			generalizer = Generalizer()
			generalizer.save_train_data(train_data)
			
			#Update hypothesis from training data
			new_weights = generalizer.train_algo(train_data, weights)
			#print("New weights:")
			#print(new_weights)
			
			#Write new weights to file
			generalizer.update_weights(new_weights)
	
	# Play AI with human
	
	#Generate experiment
	experiment = ExperimentGenerator()
	board = experiment.generate_experiment()
	#print(board)
	experiment.print_board(board)
	
	#Get weights
	weights = experiment.read_weights()
	print(weights)
	
	#Toss and initilize players
	import random
	play_first = lambda: True if random.random() >= 0.5 else False
	if play_first():
		ai = PerformanceSystem(1)
	else:
		ai = PerformanceSystem(2)
		
	#Play game till it is either won or tied
	victor = 0
	while not victor and board.count(0) > 0:
		#If human has to play first
		if ai.player_nbr == 2:
			board = ai.human_move(board, 1)
			experiment.print_board(board)
			victor = ai.evaluate_win(board)
		
		#Play AI move
		if not victor and board.count(0) > 0:
			board = ai.play_move(board, weights)
			experiment.print_board(board)
			ai.game_history.append(' '.join(map(str,board)))
			victor = ai.evaluate_win(board)
		
		#If human has to play second
		if ai.player_nbr == 1 and not victor and board.count(0) > 0:
			board = ai.human_move(board, 2)
			experiment.print_board(board)
			victor = ai.evaluate_win(board)
	
	if victor == ai.player_nbr:
		print("AI wins! Sorry, try again.")
	elif victor == 3:
		print("It is a tie!")
	else:
		print("Congrats, you win!")	
	
	print("Game over")
	
if __name__ == '__main__':
	main()