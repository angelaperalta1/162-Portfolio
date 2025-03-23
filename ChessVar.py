# Author: angela peralta
# GitHub username: angelaperalta1
# Date: 5/24/24
# Description: Create an atomic chess game. Same rules as chess however any captured piece creates an explosion on surrounding
#              8 squares except for pawns. There is also no check or checkmate, no castling, en passant, or pawn promotion


class Board:
    """
    create chess board with all pieces generated
    """
    def __init__(self):
        self._new_chessboard = {}
        self.initialize_chessboard()

    def initialize_chessboard(self):    # set board
        """
        populates brand-new chessboard with chess pieces
        """
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  # set whole board up as empty

        for row in range(8, 0, -1):
            for column in columns:
                self._new_chessboard[str(column) + str(row)] = None     # set up each spot on board as NONE
                                                                        # turn rows into a string. creating keys and setting values to None (empty)
        # load white pawns in columns + row 2
        for column in columns:
            self._new_chessboard[str(column) + '2'] = Pawn('white', self)       # self - pass current instance of chessboard. Pawn needs to be on chessboard to check state

        # load rooks in corner of board
        self._new_chessboard['a1'] = Rook('white')
        self._new_chessboard['h1'] = Rook('white')

        # load knights next to rooks
        self._new_chessboard['b1'] = Knight('white')
        self._new_chessboard['g1'] = Knight('white')

        # load bishop next to knights
        self._new_chessboard['c1'] = Bishop('white')
        self._new_chessboard['f1'] = Bishop('white')

        self._new_chessboard['d1'] = Queen('white')
        self._new_chessboard['e1'] = King('white')

        # load black pieces. black pawns
        for column in columns:
            self._new_chessboard[str(column) + '7'] = Pawn('black', self)  # self - pass current instance of chessboard. Pawn needs to be on chessboard to check state

        # load rooks in corner of board
        self._new_chessboard['a8'] = Rook('black')
        self._new_chessboard['h8'] = Rook('black')

        # load knights next to rooks
        self._new_chessboard['b8'] = Knight('black')
        self._new_chessboard['g8'] = Knight('black')

        # load bishop next to knights
        self._new_chessboard['c8'] = Bishop('black')
        self._new_chessboard['f8'] = Bishop('black')

        self._new_chessboard['d8'] = Queen('black')
        self._new_chessboard['e8'] = King('black')

    # call on print_board?

    def get_board(self):
        """
        :return: chessboard
        """
        return self._new_chessboard

    def show_board(self):
        """
        set chessboard with all pieces
        """
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # print column headings
        print('  ', end='')
        for column in columns:
            print(f' {column}  ', end='')
        print()

        # print each row
        for row in range(8, 0, -1):
            # print row number at the beginning
            print(f'{row} ', end='')
            for column in columns:
                piece = self._new_chessboard[str(column) + str(row)]
                if piece:
                    print(f'[{piece.get_name()}]', end='')  # print piece name
                else:
                    print('[  ]', end='')  # print empty square
            # print row number at the end
            print(f' {row}')

        # Print column headings again
        print('  ', end='')
        for column in columns:
            print(f' {column}  ', end='')
        print('\n')


class Moves:
    """
    store initial row and column values, used as helper function
    """
    @staticmethod
    def store_row_column(square):
        """
        store row and column inputs, create algebraic notation for square
        :return: algebraic notation of square (ex: a1)
        """

        column = ord(square[0])
        row = int(square[1])

        return column, row


class ChessPiece:
    """
    Class representing Chess Pieces: Rook, Knight, Bishop, King, Queen and Pawn.
    Includes name, color and type
    """
    def __init__(self, color):       # only take color parameter, initialize others to None for now
        self._name = None
        self._color = color
        self._type = None

    def get_type(self):
        """
        return type of piece
        """
        return self._type

    def get_color(self):
        """
        return color of piece
        """
        return self._color

    def get_name(self):     # color + type
        """
        return name of piece, which includes color and type
        """
        self._name = self._type + self._color
        return self._name


class Pawn(ChessPiece):
    """
    Pawn chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color, chess_var_obj):
        """
        pawn attributes
        :param color:
        """
        super().__init__(color)
        self._type = "pawn"
        self._name = self._color + " " + self._type     # ex "black pawn"
        self._board_object = chess_var_obj              # need to access current state of the board
        self._moves = Moves()

        # need chess var obj to access board and game state. pawn moves depend on this

    def allowed_moves(self, start, end):
        """
        allowed pawn moves, including initial moves (can move 1 or 2 forward)
        how to capture, and if at end of board it is stuck.
        :param start: current location of pawn (ex: a7)
        :param end: desired location of pawn (ex: a5)
        :return: false or move piece to end location
        """

        # calling on static method
        starting_square = self._moves.store_row_column(start)
        end_square = self._moves.store_row_column(end)

        # generate board
        game_board = self._board_object.get_board()

        # starting moves for white
        if self._color == 'white':
            if end_square[1] > starting_square[1]:
                # Check conditions for moving forward
                if starting_square[1] == 2 and end_square[1] in [3, 4] and game_board[end] is None:
                    return True
                # Check if it's a diagonal capture
                if (end_square[1] - starting_square[1]) == 1 and abs(end_square[0] - starting_square[0]) == 1 \
                        and game_board[end] is not None and game_board[end].get_color() == "black":
                    return True
                # Check if it's a regular move forward
                if starting_square[1] >= 3 and end_square[1] - starting_square[1] == 1 \
                        and end_square[0] - starting_square[0] == 0 and game_board[end] is None:
                    return True
                # Return False if none of the above conditions are met
                return False

            # Return False if trying to move backward
            if end_square[1] < starting_square[1]:
                return False

        # black pawn
        if self._color == 'black':
            if end_square[1] < starting_square[1]:
                # Check conditions for moving forward
                if starting_square[1] == 7 and end_square[1] in [5, 6] and game_board[end] is None:
                    return True
                # Check if it's a diagonal capture
                if (starting_square[1] - end_square[1]) == 1 and abs(end_square[0] - starting_square[0]) == 1 \
                        and game_board[end] is not None and game_board[end].get_color() == "white":
                    return True
                # Check if it's a regular move forward
                if starting_square[1] >= 5 and end_square[1] - starting_square[1] == -1 \
                        and end_square[0] - starting_square[0] == 0 and game_board[end] is None:
                    return True
                # Return False if none of the above conditions are met
                return False

            # Return False if trying to move backward
            if end_square[1] > starting_square[1]:
                return False


class Rook(ChessPiece):
    """
    Rook chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color):      # don't need chessvar obj b/c don't need boardgame
        super().__init__(color)
        self._type = "rook"
        self._color = color
        self._name = self._color + " " + self._type         # ex "black pawn"
        self._moves = Moves()

    def allowed_moves(self, start, end):
        """
        allowed rook moves. can move vertically or horizontally
        :param start: starting square notation
        :param end: end square notation
        :return: True if the move is legal. False if the move is illegal.
        """

        #FIXME
        starting_square = Moves.store_row_column(start)
        end_square = Moves.store_row_column(end)

        # if row same, moving horizontally. if column same, moving vertically

        # allowed moves for white rook
        if self._color == 'white':
            if (end_square[1] - starting_square[1]) == 0 or (end_square[0] - starting_square[0]) == 0:
                return True
            else:
                return False

        # allowed moves for black rook
        if self._color == 'black':
            if (end_square[1] - starting_square[1]) == 0 or (end_square[0] - starting_square[0]) == 0:      # move any num of spaces up/down left/right
                return True
            else:
                return False


class Knight(ChessPiece):
    """
    knight chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color):      # don't need chessvar obj b/c don't need boardgame
        super().__init__(color)
        self._type = "knight"
        self._color = color
        self._name = self._color + " " + self._type         # ex "black pawn"
        self._moves = Moves()

    def allowed_moves(self, start, end):
        """
        allowed moves for a Knight chesspiece
        :param start: starting square notation
        :param end: end square notation
        :return: True if the move is legal. False if the move is illegal.
        """

        starting_square = self._moves.store_row_column(start)
        end_square = self._moves.store_row_column(end)

        # up/down 2, left right 1 (L)
        if abs(end_square[1] - starting_square[1]) == 2 and abs(end_square[0] - starting_square[0]) == 1:
            return True
        # up/down 1, left/right 2 (L)
        if abs(end_square[1] - starting_square[1]) == 1 and abs(end_square[0] - starting_square[0]) == 2:
            return True
        else:
            return False


class Bishop(ChessPiece):
    """
    bishop chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color):              # don't need chess var obj b/c don't need boardgame
        super().__init__(color)
        self._type = "bishop"
        self._color = color
        self._name = self._color + " " + self._type         # ex "black pawn"
        self._moves = Moves()

    def allowed_moves(self, start, end):
        """
        allowed moves for bishop chess piece. only move diagonally
        :param start: starting square notation
        :param end: end square notation
        :return: True if the move is legal. False if the move is illegal.
        """

        # static method
        starting_square = self._moves.store_row_column(start)
        end_square = self._moves.store_row_column(end)

        # use abs since tracking how many moves total, since can move any amount of spaces
        if abs(end_square[1] - starting_square[1]) == abs(end_square[0] - starting_square[0]):
            return True
        else:
            return False


class King(ChessPiece):
    """
    king chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color):                  # don't need chess var obj b/c don't need boardgame
        super().__init__(color)
        self._type = "king"
        self._color = color
        self._name = self._color + " " + self._type         # ex "black pawn"
        self._moves = Moves()

    def allowed_moves(self, start, end):
        """
        allowed moves for a King chess piece
        :param start: starting square notation
        :param end: end square notation
        :return: True if the move is legal. False if the move is illegal.
        """

        starting_square = self._moves.store_row_column(start)
        end_square = self._moves.store_row_column(end)

        row_diff = abs(end_square[1] - starting_square[1])
        col_diff = abs(end_square[0] - starting_square[0])

        # Check if the move is within the king's range (1 square in any direction)
        if row_diff <= 1 and col_diff <= 1:
            return True
        else:
            return False

class Queen(ChessPiece):
    """
    queen chess piece, subclass of Chess Piece. Includes type, color, name
    """
    def __init__(self, color):                  # don't need chess var obj b/c don't need boardgame
        super().__init__(color)
        self._type = "queen"
        self._color = color
        self._name = self._color + " " + self._type         # ex "black pawn"
        self._moves = Moves()

    def allowed_moves(self, start, end):
        """
        allowed moves for queen. any direction and any amount of squares
        :param start: starting square notation
        :param end: end square notation
        :return: True if the move is legal. False if the move is illegal.
        """

        starting_square = self._moves.store_row_column(start)
        end_square = self._moves.store_row_column(end)

        # check if same row column or diag move
        row_difference = abs(end_square[1] - starting_square[1])
        col_difference = abs(end_square[0] - starting_square[0])

        if (starting_square[0] == end_square[0] or starting_square[1] == end_square[1] or
                row_difference == col_difference):
            return True
        else:
            return False


class ChessVar:
    """
    Atomic Chess - all starting positions and rules are the same as regular chess EXCEPT that any captured piece creates an
    explosion surrounding the 8 squares of the captured piece except for pawns, the capturing piece is also affected.
    There is also no castling, en passant or pawn promotion. The overall goal is still to capture the king.
    """

    def __init__(self):
        self._board = self.initialize_board()  # Initialize the board
        self._game_state = "UNFINISHED"
        self._current_player = "white"
        self._used_pieces = []      # if king is in here, game over

    def get_board(self):
        """
        get chessboard
        """
        return self._board

    def get_used_pieces(self):
        """
        :return: used pieces
        """
        return self._used_pieces

    def initialize_board(self):
        """
        Initialize the board.
        """
        board_instance = Board()  # board instance
        return board_instance.get_board()  # get board

    def get_game_state(self):
        """
        :return: UNFINISHED, WHITE WON, BLACK WON
        """
        return self._game_state

    def update_game_state(self):
        """
        update current game state. if black king is in used pieces, white wins, vice versa
        """

        self._game_state = 'UNFINISHED'

        for piece in self._used_pieces:
            # if current player is white
            if self._current_player == 'white':
                if piece.get_type() == 'king' and piece.get_color() == 'black':
                    self._game_state = "WHITE_WON"
                    return
            # if current player is black
            if self._current_player == 'black':
                if piece.get_type() == 'king' and piece.get_color() == 'white':
                    self._game_state = "BLACK_WON"
                    return

    def current_player_winner(self):
        """
        current player is winner
        """
        if self._current_player == 'WHITE':
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'BLACK_WON'

    def get_current_player(self):
        """
        :return: current player, white or black
        """
        return self._current_player

    def change_player(self):
        """
        change players. ex; if white turn, change to black and vice versa
        """
        if self._current_player == "white":
            self._current_player = "black"
        else:
            self._current_player = 'white'

    def make_move(self, start, end):
        """
        take 2 parameters - strings representing square being moved from and square moved to
        """
#        print("Calling make_move")
        # Print the game state:
#        print(f"Game state: {self._game_state}")
        # Print the current player:
#        print(f"Current player: {self._current_player}")
        # Print the value of each argument (start, end):
#        print(f"Move: {start} {end}")
#        print("The current state of the board:")
#        self.print_board()

        # check if game is over
        if self._game_state != 'UNFINISHED':
            print(self.get_game_state())
            return False

        # no more than 2 string entries, must be valid entry
        if len(start) != 2 or len(end) != 2:
            return False

        # store alg notation
        start_col = start[0]
        start_row = int(start[1])
        end_col = end[0]
        end_row = int(end[1])

        if (start_col not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] or
                end_col not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] or
                start_row not in [1, 2, 3, 4, 5, 6, 7, 8] or
                end_row not in [1, 2, 3, 4, 5, 6, 7, 8]):
            print("Not a valid move!!")
            return False

        # if current player chose opponent piece, return false
        if self._current_player != self._board[start].get_color():
            return False

        # if player didn't choose a piece, return false
        if not self._board[start]:
            print("No piece chosen")
            return False

        # player start and end are the same, piece did not move. must be different
        if start == end:
            print("You didn't move the piece")
            return False

        # check if move is valid based on chess piece and current player
        if not self._board[start].allowed_moves(start, end):
            return False

        # player can't move through another chess piece unless knight
        if self._board[start].get_type() != 'knight' and not self.move_along_board(start, end):
            return False

        # if end square has same color piece as starting piece
        if self._board[end] is not None and self._board[end].get_color() == self._board[start].get_color():
            return False

        # cant remove own piece
        if self._board[end] and self._current_player == self._board[end].get_color():
            return False

        # king cant capture
        if (self._board[start].get_type() == 'king' and self._board[end] is not None and
                self._board[end].get_color() != self._board[start].get_color()):
            print("King cannot capture pieces")
            return False

        # if there is a piece on the end square and end square color is not the current player
        if self._board[end] is not None and self._board[end].get_color() != self._current_player:
            # Capture the enemy piece
            captured_piece = self._board[end]
            capturing_piece = self._board[start]

            if captured_piece.get_type() != 'pawn':
                # trigger explosion around the captured square
                self.explode_around_square(end)
            
                # add both captured and capturing piece to used list
                self._used_pieces.append(captured_piece)
                self._used_pieces.append(capturing_piece)
            
                # remove both pieces from board
                self._board[end] = None
                self._board[start] = None
            
                self.update_game_state()
                return True

            # if end piece contains a pawn, dont trigger explosion.
            if captured_piece.get_type() == 'pawn':
                captured_piece = self._board[end]
                capturing_piece = self._board[start]
                self._used_pieces.append(captured_piece)
                self._used_pieces.append(capturing_piece)

            # if the king is captured directly by a piece other than a king

            if captured_piece.get_type() == 'king':
                self.current_player_winner()
                self.update_game_state()
                return True

            if self._game_state != 'UNFINISHED':
                return True

        # legal move, make move update board
        self._board[end] = self._board[start]
        self._board[start] = None  # Clear the starting square

        self.change_player()

        return True

    def explode_around_square(self, captured_square):
    """
    8 squares surrounding captured piece explode and are added to used_pieces.
    Pawns are only destroyed if they are at the center. If a king explodes, end game.
    """
    column = captured_square[0]
    row = int(captured_square[1])

    col_index = ord(column)
    row_index = int(row)

    row_offsets = [-1, 0, 1]
    col_offsets = [-1, 0, 1]

    for row_offset in row_offsets:
        for col_offset in col_offsets:
            new_col_index = col_index + col_offset
            new_row_index = row_index + row_offset

            # skip if out of bounds
            if not (ord('a') <= new_col_index <= ord('h') and 1 <= new_row_index <= 8):
                continue

            square = chr(new_col_index) + str(new_row_index)
            piece = self._board.get(square)

            if piece:
                # Only the center pawn survives the explosion
                if piece.get_type() == 'pawn' and square != captured_square:
                    continue

                self._used_pieces.append(piece)
                self._board[square] = None

                # If a king is caught in the explosion, update game state
                if piece.get_type() == 'king':
                    self.current_player_winner()
                    self.update_game_state()


    def print_board(self):
        """
        :return: current state of the board, helpful for testing
        """
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        column_headings = '   ' + '  '.join(columns) + '  '
        print(column_headings)

        # Print each row and columns
        for row in range(8, 0, -1):
            row_pieces = [
                f"[{self._board[column + str(row)].get_name() if self._board[column + str(row)] else '  '}]"
                for column in columns
            ]
            row_line = f"{row} {' '.join(row_pieces)} {row}"
            print(row_line)
        print(column_headings)

    def move_along_board(self, start, end):
        """
        moving in all directions on board
        """
        start_column, start_row = ord(start[0]), int(start[1])
        end_column, end_row = ord(end[0]), int(end[1])

        # vertical move
        if start_column == end_column:
            return self.is_clear_vertical(start, end)

        # horizontal move
        if start_row == end_row:
            return self.is_clear_horizontal(start, end)

        # diagonal move
        if abs(start_row - end_row) == abs(start_column - end_column):
            return self.is_clear_diagonal(start, end)

        return True     # or return False?

    def is_clear_vertical(self, start, end):
        """
        Check vertical moves.
        """
        start_column, start_row = ord(start[0]), int(start[1])
        end_column, end_row = ord(end[0]), int(end[1])

        # vertical moves
        if (end_column - start_column) == 0:
            if (end_row - start_row) > 0:       # 1 to 8
                for row in range(1, end_row - start_row):
                    if self._board[chr(start_column) + str(start_row + row)]:
                        return False
            if (start_row - end_row) > 0:
                for row in range(1, start_row - end_row):
                    if self._board[chr(start_column) + str(start_row - row)]:
                        return False
            return True

    def is_clear_horizontal(self, start, end):
        """
        Check horizontal moves.
        """
        start_column, start_row = ord(start[0]), int(start[1])
        end_column, end_row = ord(end[0]), int(end[1])

        if (end_row - start_row) == 0:
            if (end_column - start_column) > 0:      # a to h
                for column in range(1, end_column - start_column):
                    if self._board[chr(start_column + column) + str(start_row)]:
                        return False
            if (start_column - end_column) > 0:
                for column in range(1, start_column - end_column):
                    if self._board[chr(start_column - column) + str(start_row)]:
                        return False
            return True

    def is_clear_diagonal(self, start, end):
        """
        Check diagonal moves.
        """
        start_column, start_row = ord(start[0]), int(start[1])
        end_column, end_row = ord(end[0]), int(end[1])

        # move is diagonal - up right
        if (end_row - start_row) == (end_column - start_column):
            if (end_row - start_row) > 0 and (end_column - start_column) > 0:
                for square in range(1, end_row - start_row):
                    if self._board[chr(start_column + square) + str(start_row + square)]:
                        return False
                return True
                # up left
            if (end_row - start_row) > 0 and (start_column - end_column) > 0:
                for square in range(1, end_row - start_row):
                    if self._board[chr(start_column + square) + str(start_row + square)]:
                        return False
                return True
                # down right
            if (start_row - end_row) > 0 and (end_column - start_column) > 0:
                for square in range(1, start_row - end_row):
                    if self._board[chr(start_column + square) + str(start_row - square)]:
                        return False
                return True
                # down left
            if (start_row - end_row) > 0 and (start_column - end_column) > 0:
                for square in range(1, start_row - end_row):
                    if self._board[chr(start_column + square) + str(start_row - square)]:
                        return False
                return True
