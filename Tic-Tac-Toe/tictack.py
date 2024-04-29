class tic_tac_toe():
    def __init__(self):
        # board is a list of blank spaces ranging from 0-9
        self.board = [' ' for i in range(9)]
        # current player (default value is X)
        self.current_player = 'X'
        
    # printing the tic-tac-toe board
    #parameter means its only calling the class itself?
    def print_ttt_board(self):
        # print all 3 rows by splicing the list
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        
    # check if a player has won
    def check_winner(self):
        # these are all the possible winning combinations in tic-tac-toe
        winners = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
        # loop through each sublist in the list
        for win in winners:
            # the board will only contain 'X', 'O', or ' '
            # so we check if the X's or the O's create a winning combination
            if self.board[win[0]] == self.board[win[1]] == self.board[win[2]] != ' ':
                self.print_ttt_board()
                return True
        
        return False
        
    # check if board is full and there are no winners
    def catscratch(self):
        # returns true if board is full i.e. no more ' ' in the board
        return ' ' not in self.board
        
    # function to run the game and includes error handling
    def play(self, position):
        # check if current value in position is empty
        if self.board[position] == ' ':
            # insert value at position
            self.board[position] = self.current_player
            
            # check if there is a winner
            if self.check_winner():
                print(f'Player {self.current_player} won!')
                return True
            # check if board is full
            elif self.catscratch():
                print('There are no winners in this game!')
                return True
            
            # change player turn
            else:
                #self.current_player = 'X' if self.current_player == 'O' else 'O'
                if self.current_player == 'X':
                    self.current_player = 'O'
                else:
                    self.current_player = 'X'
            return False
        # invalid non-empty position was selected
        else:
            print('Invalid move! Please input an empty position')
            return False
            
if __name__ == "__main__":
    game = tic_tac_toe()
    
    while True:
        game.print_ttt_board()
        position = input(f'Player {game.current_player}, turn. Select a position between 0-8: ')
        if game.play(int(position)):
            break








class tic_tac_toe_master():
    # initializing variables
    # this is correct
    def __init__(self):
        # board is a list of blank spaces ranging from 0-9
        self.board = ['X', ' ', 'O', 'X', ' ', 'X', 'O', ' ', ' '] # default board for testing
        # current player (default value is X)
        self.current_player = 'human'
        self.ai = 'X'
        self.human = 'O'
        # a list of all the indexes with empty values (no X or O) on the board
        self.empties = [] # should be part of function, not entire class?
    
    # finds all the empty spots on the board
    # this is correct
    def find_empties(self):
        # inserts indexes to the array if it is empty i.e. X or O hasn't been placed
        self.empties = [i for i in range(9) if self.board[i] not in ['X', 'O']]
        
    # printing the tic-tac-toe board
    #parameter means its only calling the class itself?
    #this is correct
    def print_ttt_board(self):
        # prints the list by slicing the board into three rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    # check if a player has won
    # this is correct
    def check_winner(self, player):
        # these are all the possible winning combinations in tic-tac-toe
        # this is a list of tuples
        winners = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
        # loop through each sublist in the list
        for win in winners:
            # the board can only contain 'X', 'O', or ' '
            # so we check if the X's or the O's create a winning combination
            if self.board[win[0]] == self.board[win[1]] == self.board[win[2]] == player:
                self.print_ttt_board()
                print('\n') # added so output is less messy while testing
                # there is a winning combination
                return True
        # there is no winning combination
        return False
    
    # check if board is full and there are no winners
    # this is correct
    def catscratch(self):
        # returns true if board is full i.e. no more ' ' in the board
        return ' ' not in self.board
    
    # this function helps the ai choose the best play
    # through recursive calls and returns a dictionary
    # it basically plays through the entire game with itself and 
    # looks at every possible option and then returns the best play
    def minimax(self, player):
        # update the empties list
        self.find_empties()
        
        # these 3 returns return a dictionary that holds a score
        # the score determines which play we choose
        # only the leaf nodes (plays that end the game) will be returned here
        
        # check to see if human won
        if self.check_winner(self.human):
            # score of -1 = human is winning
            return {'score': -1}
        # check to see if ai won
        elif self.check_winner(self.ai):
            # score of 1 = ai is winning
            return {'score': 1}
        # catscratch function here?
        # check to see if no winners and empties list is empty (no empty indexes on board)
        elif not self.empties:
            # score of 0 = board is full and no winners
            return {'score': 0}
        
        # stores a list of potential moves as dictionaries for the current state of the game
        # the number of empty positions is the number of plays in the plays list
        plays = []
        
        # iterate through each empty position in the board
        for index in self.empties:
            # dictionary that has the index and score of a play
            # this is like the main dictionary, the 3 returns from above
            # returns a score dictionary that we will then insert here
            play = {}
            # set play's index value to the index
            play['index'] = index
            # insert player move to the board
            self.board[index] = player
            
            # checking if player is the ai
            if player == self.ai:
                # recursively call the minimax function to get the
                # best score of that play, also change turn to human
                result = self.minimax(self.human)
                # set play's score value to result's score value
                play['score'] = result['score']
            
            # checking if player is the human 
            else:
                # recursively call the minimax function to get the
                # best score of that play, also change turn to ai
                result = self.minimax(self.ai)
                # set play's score value to result's score value
                play['score'] = result['score']
            
            # reverting board since we only needed to change board for the recursive call
            # creating a temporary board for the current state is probably better than this
            self.board[index] = ' '
            # insert the move/play to the plays list
            plays.append(play)
        
        # the current player is the ai
        if player == self.ai:
            # holds best score from plays, defaults to -inf on purpose
            # since having the biggest score is best for the ai
            best_score = -float("inf")
            
            # iterate through all the different plays in the playlist
            # i.e. all the potential positions on the board and their scores
            for play in plays:
                # check to see if the current play's score is greater than best score
                if play['score'] > best_score:
                    # set the best score to the current play's score
                    best_score = play['score']
                    # set the best play to the current play
                    best_play = play
        # the current player is the human
        else:
            # holds best score from plays, defaults to inf on purpose
            # since having the lowest score is best for the human
            best_score = float("inf")
            
            # iterate through all the different plays in the playlist
            # i.e. all the potential positions on the board and their scores
            for play in plays:
                # check to see if the current play's score is less than best score
                if play['score'] < best_score:
                    # set the best score to the current play's score
                    best_score = play['score']
                    # set the best play to the current play
                    best_play = play
        
        # returns a dictionary of the best play
        return best_play
    
    # not sure if correct
    def play(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.human
            
            if self.check_winner(self.human):
                print(f'Player {self.human} won!')
                return True
            # checking if there are no indexes that are empty
            elif not any(cell == ' ' for cell in self.board):
                print("It's a draw")
                return True
                
            else:
                ai_move = self.minimax(self.ai)['index']
                self.board[ai_move] = self.ai
                if self.check_winner(self.ai):
                    print(f'Player {self.ai} won!')
                    return True
                elif not any(cell == ' ' for cell in self.board):
                    print("It's a draw")
                    return True
                return False
        else:
            print('Invalid move. Try again')
            return False

# starts the tic-tac-toe game
if __name__ == "__main__":
    game = tic_tac_toe_master()
    
    # running game until there is a winner or board is full
    while True:
        game.print_ttt_board()
        # human player's turn
        while True:
            # error handling for player
            try:
                # getting index from user
                position = int(input("Enter your move 0-8: "))
                # check to see if position is valid
                if 0 <= position <= 8 and game.board[position] == ' ':
                    break
                # position is invalid
                else:
                    print("Invalid move.")
            # error on input. non-number input
            except ValueError:
                print("Invalid Input. Please enter a num")
        
        # inserting human's move to the board
        game.board[position] = game.human
        
        # check if the human won the game
        if game.check_winner(game.human):
            print(f'Player {game.human} wins!')
            break
        #catscratch?
        # check to see if the board is full
        elif all(cell != ' ' for cell in game.board):
            # board is full and no winners mean a draw
            print("it's a draw lol")
            break
        
        # printing board with human's turn
        game.print_ttt_board()
        print('\n\n\n\n')
        
        # so we never call play, we instead just call minimax
        # I think this is good since I need to test the function
        # minimax returns a dictionary so we just want the value (int) stored in the index key
        # that value is the index of where the ai is inserting its move
        ai_move = game.minimax(game.ai)['index']
        print(type(ai_move))
        print(f'ai chose index: {ai_move}')
        # inserting ai's move to the board
        game.board[ai_move] = game.ai
        
        if game.check_winner(game.ai):
            print(f'Player {game.ai} wins!')
            break
        elif all(cell != ' ' for cell in game.ai):
            print("it's a draw lol")
            break