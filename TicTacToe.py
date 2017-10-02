
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
def get_featureset(board)
	#initialize x0 = 1
	featureset = [1]
	#x1 = number of turns
	featureset.append(sum(1 for elem in board if elem = 1))
	#x2 = number of open lines - player 1
	#x3 = number of open lines - player 2
	#x4 = number of open lines with 2 or more tokens - player 1
	#x5 = number of open lines with 2 or more tokens - player 2
	#x6 = number of points with 2 or more open lines - player 1
	#x7 = number of points with 2 or more open lines - player 2
	return featureset
	
# Calculate board score
def board_score(board):
	return 5
	
	
# Performance System:
# Given initial board, generates game history
def play_game(board):
	#Count number of blank spaces on board
	open_spaces = sum(1 for elem in board if not elem)
	print("Open spaces=" + str(open_spaces))
	
	max_score = 0

	#For each space where next token can be added
	#Identify moves for opponent
	#For each space and opponent move. calculate board score
	#Keep track of board with max score and select it as my move	
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
	board[move] = 1
	print_board(board)
	if (evaluate_win(board)):
		pass
		
	
	#Ask for opponent move
	opponent_move = input("Enter your move..")
	
	#Apply opponent move
	board[int(opponent_move)]= 2
	print_board(board)
	if (evaluate_win(board)):
		pass
	
		
# Check board for victory condition
def evaluate_win(board):
	win_indices = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
	victor = 0
	for row in win_indices:
		board_slice = [board[idx] for idx in row]
		if len(set(board_slice)) == 1:
			victor = set(board_slice).pop()
			break
	if victor == 1:
		print("Sorry, you lost!")
	if victor == 2:
		print("Congrats, you won!")
	return victor
	
# Main function
def main():
	board = generate_experiment()
	#print(board)
	print_board(board)
	play_game(board)
	

if __name__ == '__main__':
	main()