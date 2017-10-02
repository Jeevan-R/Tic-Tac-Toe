#Global constants and variables
WIN_INDICES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
TOKEN_XREF = [[0, 3, 6], [0,4], [0, 5, 7], [1,3], [1, 4, 6, 7], [1, 5], [2, 3, 7], [2, 4], [2, 5, 6]]
weights = [0.01] * 8

# Experiment Generator:
# Generate first board
def generate_experiment():
	board = [0] * 9
	return board
	
# Print board
# Player 1 = X
# Player 2 = O
# Blank spaces 0 = _
def print_board(board):
	print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[0:3]]))
	print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[3:6]]))
	print(' '.join(['X' if elem == 1 else 'O' if elem == 2 else '_' for elem in board[6:9]]))
	print()

# Convert board to feature set
def get_featureset(board):
	#initialize x0 = 1
	featureset = [1]
	
	#x1 = number of turns
	featureset.append(sum(1 for elem in board if elem == 1))
	
	#x2 = number of open lines - player 1
	#x3 = number of open lines - player 2
	#x4 = number of open lines with 2 or more tokens - player 1
	#x5 = number of open lines with 2 or more tokens - player 2
	x2, x3, x4, x5 = 0, 0, 0, 0
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
				if len(board_slice) > 1:
					x4 += 1
			else :
				x3 += 1
				p2_lines.append(1)
				p1_lines.append(0)
				if len(board_slice) > 1:
					x5 += 1
		else :
			p1_lines.append(0)
			p2_lines.append(0)
	#print("attrib 2-5: " + str(x2) + " " + str(x3) + " " + str(x4) + " " + str(x5))
	
	#x6 = number of points with 2 or more open lines - player 1
	#x7 = number of points with 2 or more open lines - player 2
	x6, x7 = 0, 0
	import operator
	#print(p1_lines)
	#print(p2_lines)
	if p1_lines.count(1) or p2_lines.count(1):
		for row in TOKEN_XREF:
			if p1_lines.count(1):
				if operator.itemgetter(*row)(p1_lines).count(1) > 1:
					x6 += 1
			if p2_lines.count(1):
				if operator.itemgetter(*row)(p2_lines).count(1) > 1:
					x7 += 1
	
	#Construct and return featureset
	featureset.extend([x2, x3, x4, x5, x6, x7])
	return featureset
	
	
# Calculate board score
def board_score(board):
	#Convert board to featureset
	attributes = get_featureset(board)
	#print("Board attributes: ")
	#print(board)
	#print(attributes)
	#print(sum([w*a for w, a in zip(weights, attributes)]))
	
	#Compute and return rating
	return sum([w*a for w, a in zip(weights, attributes)])
	
	
# Performance System:
# Given initial board, generates game history
def play_game(board):
	victor = 0
	game_history = []
	
	while not victor and board.count(0) > 0:
		#Play my move
		board = play_move(board)
		print_board(board)
		game_history.append(''.join(map(str,board)))
		victor = evaluate_win(board)
		
		#Ask for opponent move if victor is not decided
		if not victor:
			opponent_move = input("Enter your move..")
			
			#Apply opponent move
			board[int(opponent_move)]= 2
			print_board(board)
			game_history.append(''.join(map(str,board)))
			victor = evaluate_win(board)
	
	return victor, game_history

# Pick and play best move
def play_move(board):
	max_score = 0

	#Count number of blank spaces on board
	open_spaces = sum(1 for elem in board if not elem)
	#print("Open spaces=" + str(open_spaces))
	
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
				next_board[idx] = 1
				#Iterate thru possible opponent moves
				for nb_idx, nb_elem in enumerate(next_board):
					if not nb_elem:
						#Mark opponent move
						next_board[nb_idx] = 2
						#print_board(next_board)
						#Calculate board score
						score = board_score(next_board)
						#Reset opponent move
						next_board[nb_idx] = 0
						#Check max score
						if score > max_score:
							max_score = score
							move = idx
		
		#Select move with highest board score
		if max_score > 0:
			board[move] = 1
	
	#If only one space is available, select it for next move
	elif open_spaces == 1:
		board[board.index(0)] = 1
	
	return board
	
# Check board for victory condition
def evaluate_win(board):
	victor = 0
	for row in WIN_INDICES:
		board_slice = [board[idx] for idx in row]
		if len(set(board_slice)) == 1:
			victor = set(board_slice).pop()
			break
	if not victor and not board.count(0):
		victor = 3
	return victor

# Critic
# Given game history, generates training examples	
def generate_train_data(victor, game_history):
	pass
	
# Main function
def main():
	#Generate experiment
	board = generate_experiment()
	#print(board)
	print_board(board)
	
	#Play game till it is either won or tied
	victor, game_history = play_game(board)
	print(game_history)
	if victor == 1:
		print("Sorry, you lost!")
	elif victor == 2:
		print("Congrats, you won!")
	elif victor == 3:
		print("It is a tie!")

	#Convert game history to training examples
	train_data = generate_train_data(victor, game_history)
	
	
if __name__ == '__main__':
	main()