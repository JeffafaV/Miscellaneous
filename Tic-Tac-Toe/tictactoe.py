# updated code
import random

class tic_tac_toe():
    # initializes tic_tac_toe class objects
    def __init__(self):
        # board is a list of blank spaces ranging from 0-9
        self.board = [' ' for i in range(9)]
        self.player_1 = 'X' # marker for player 1
        self.player_2 = 'O' # marker for player 2
        
    # printing the tic-tac-toe board
    #parameter means its only calling the class itself?
    def print_board(self):
        # print all 3 rows by splicing the list
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        
    # check if a player has won
    def check_winner(self, current_player, current_board):
        # these are all the possible winning combinations in tic-tac-toe
        winners = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
        # loop through each sublist in the list
        for win in winners:
            # the board will only contain 'X', 'O', or ' '
            # so we check if the X's or the O's create a winning combination
            if current_board[win[0]] == current_board[win[1]] == current_board[win[2]] == current_player:
                return True
        
        # there is no winning combination
        return False
        
    # check if board is full and there are no winners
    def board_full(self, current_board):
        # returns true if board is full i.e. there are no ' ' on the board
        return ' ' not in current_board
    
    # switches between player 1 and player 2
    def switch_players(self, current_player):
        # check if current player is player 1
        if current_player == self.player_1:
            # switch to player 2
            return self.player_2
        # check if current player is player 2
        else:
            # switch to player 1
            return self.player_1
        
    # inserts a play to the board for the human player
    def player_move(self, current_player):
        # loops until user inputs a valid input
        while True:
            # checks to see if code in body is valid (i.e. input is actually an int)
            try:
                position = int(input(f'Player {current_player} turn. Select a position between 0-8: '))
            
            # invalid data type was detected
            except ValueError:
                print("Invalid input. Enter a whole number")
                
            # position input is not in range of board indexes (0 - 8)
            if position < 0 or position > 8:
                print('Invalid position. Select a position between 0-8')
            
            # position chosen is already filled from a previous play
            elif self.board[position] != ' ':
                print('Invalid position. Select an empty position')
            
            # position input is valid
            else:
                break
        
        # insert player's play to the board at given position
        self.board[position] = current_player
    
    # returns a list of empty positions (indexes) on the board
    def find_empties(self, current_board):
        # creates a list of all the empty positions on the board
        empties = [i for i in range(9) if current_board[i] not in [self.player_1, self.player_2]]
        return empties
    
    # inserts a random play to the board for the computer player
    def computer_move_random(self, current_player):
        # get the list of empty positions
        empties = self.find_empties(self.board)
        # choose a position from that list of empty positions
        position = random.choice(empties)
        print(f'Player {current_player} turn. Player {current_player} chose: {position}')
        
        # insert computer's play to the board at given position
        self.board[position] = current_player

    # inserts an optimal play to the board for the computer player
    def computer_move_minimax(self, current_player):
        # utilize the minimax algorithm to get the best position to play
        position = self.minimax(current_player, self.board)['index']
        print(f'Player {current_player} turn. Player {current_player} chose: {position}')

        # insert computer's play to the board at given position
        self.board[position] = current_player
    
    # this ai algorithm helps the computer choose the best play through recursive calls and returns a dictionary
    # it plays through the entire game with itself, looks at every possible option, and then returns the best play/position
    def minimax(self, current_player, current_board):
        # these 3 returns return a dictionary that holds a score
        # the score determines which play we choose
        # only the leaf nodes (plays that end the game) will be returned here
        # score of -1 = human wins
        # score of 1 = ai wins
        # score of 0 = board is full and no winners
        
        # check to see if human won
        if self.check_winner(self.player_1, current_board):
            return {'score': -1}
        
        # check to see if ai won
        elif self.check_winner(self.player_2, current_board):
            return {'score': 1}
        
        # check to see if no winners and empties list is empty (no empty indexes on board)
        elif self.board_full(current_board):
            return {'score': 0}
        
        # get a list of all the empty positions for the current board
        empties = self.find_empties(current_board)

        # stores a list of potential moves as dictionaries for the current state of the game
        # the number of empty positions is the number of plays in the plays list
        plays = []
        
        # iterate through each empty position in the board
        for index in empties:
            temp_board = current_board.copy()
            # dictionary that has the index and score of a play
            # this is like the main dictionary, the 3 returns from above
            # returns a score dictionary that we will then insert here
            play = {}
            # set play's index value to the index
            play['index'] = index
            # insert player move to the board
            temp_board[index] = current_player
            
            # checking if player is the ai/computer
            if current_player == self.player_2:
                # recursively call the minimax function to get the
                # best score of that play, also change turn to human
                result = self.minimax(self.player_1, temp_board)
                # set play's score value to result's score value
                play['score'] = result['score']
            
            # checking if player is the human 
            else:
                # recursively call the minimax function to get the
                # best score of that play, also change turn to ai
                result = self.minimax(self.player_2, temp_board)
                # set play's score value to result's score value
                play['score'] = result['score']
            
            # insert the move/play to the plays list
            plays.append(play)
        
        # the current player is the ai/computer
        if current_player == self.player_2:
            # holds best score from plays, defaults to -inf on purpose
            # since having the highest score is best for the ai
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
        
        # it's kind of difficult to understand why we want to get the best score/play of the human player 
        # when we only need the best score/play of the ai player. Since the minimax algorithm goes through all 
        # possibilities as both ai and human we assume that both the ai and human player will choose the best 
        # play for them to win. So before choosing the best play for the ai, the algorithm has to look what the 
        # best play is for the human player and then choose the oposite. It is basically a chain of one player 
        # choosing the best play for themselves which is also the worst play for the other player.
        
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
    
    # function to run the game and includes error handling
    def play(self):
        # keeps track of players turn
        # set it to player 1 since they go first
        current_player = self.player_1
        players = int(input('Insert 1 for single player or 2 for multiplayer: '))
        
        # keeps looping until there is a winner or a tie
        while True:
            # print the current state of the board
            self.print_board()
            
            # player 1 is the current player
            if current_player == self.player_1:
                self.player_move(current_player)
            
            # player 2 is the current player
            else:
                # single player
                if players == 1:
                    # computer move
                    #self.computer_move_minimax(current_player)
                    self.computer_move_random(current_player)
                    
                # two players
                else:
                    self.player_move(current_player)
            
            # check if there is a winner
            if self.check_winner(current_player, self.board):
                self.print_board()
                print(f'Player {current_player} wins!')
                break
            # check if there is a tie
            # there's a tie if there are no winners and board is full
            elif self.board_full(self.board):
                self.print_board()
                print("It's a tie!")
                break
            
            # switch players turn
            current_player = self.switch_players(current_player)
            
if __name__ == "__main__":
    # create a tic-tac-toe object
    game = tic_tac_toe()
    print('Welcome to Tic-Tac-Toe!')
    # play tic-tac-toe
    game.play()
    