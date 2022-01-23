from os import path
from chess_player import ChessPlayer
import random
from copy import deepcopy
import numpy as np


class aahmad3_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.last_move = []
        self.became_queen = False
        self.count = 0
        self.see = 0

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        my_color = 0
        opp_color = 0
        if self.color == "white":
            my_color = "white"
            opp_color = "black"
        else:
            my_color = "black"
            opp_color = "white"

        temp_boards = deepcopy(self.board)

        if len(self.last_move) > 0 and self.count > 0 and self.last_move[1] in temp_boards and "queen" in temp_boards[self.last_move[1]].name:
            self.became_queen = True
        available_moves = temp_boards.get_all_available_legal_moves(my_color)
        best_move = 0
        best_move_alpha = []
        old_opp_score = self.get_total_score(temp_boards,opp_color)
        for move in available_moves:
            second_temp_board = deepcopy(temp_boards)
            second_temp_board.make_move(move[0], move[1])
            if len(second_temp_board.get_all_available_legal_moves(opp_color)) == 0 and second_temp_board.is_king_in_check(opp_color) == False:
                continue
            if second_temp_board.is_king_in_checkmate(opp_color):
                best_move = move
                return best_move
            opp_score = self.get_total_score(second_temp_board,opp_color)
            some_move = self.evaluate2(second_temp_board, old_opp_score, opp_score, opp_color, my_color)
            some_move_alpha = [some_move, move]
            best_move_alpha.append(some_move_alpha)
        best_move = self.which_is_the_best_move(best_move_alpha, temp_boards, opp_color)
        self.count = self.count + 1
        return best_move

    def evaluate2(self, temp_board, old_opp_score, opp_score, opp_color, my_color):
        score = self.get_total_score(temp_board, self.color)
        difference = old_opp_score - opp_score
        check = []
        moves_black = temp_board.get_all_available_legal_moves(opp_color)
        for move in moves_black:
            second_temp_board = deepcopy(temp_board)
            second_temp_board.make_move(move[0], move[1])
            new_score = self.get_total_score(second_temp_board, my_color)
            if second_temp_board.is_king_in_checkmate(my_color):
                return 0, -100000, len(moves_black)
            diff = score - new_score
            check_score = difference - diff
            check.append(check_score)

        best_outcome = check[0]
        worst_outcome = check[0]
        for i in range(len(check)):
            if check[i] > best_outcome:
                best_outcome = check[i]
            if check[i] < worst_outcome:
                worst_outcome = check[i]

        return best_outcome, worst_outcome, len(moves_black)

    def which_is_the_best_move(self, best_move_alpha, tempboards, oppcolor):
        if isinstance(best_move_alpha, list):
            best_move_list = []
            for i in range(len(best_move_alpha)):
                sum = best_move_alpha[i][0][0] + best_move_alpha[i][0][1]
                best_move_list.append([sum, best_move_alpha[i][1], best_move_alpha[i][0][2]])
            first = best_move_list[0][1]
            best_sum = best_move_list[0][0]
            best_move = first
            best_length = best_move_list[0][2]
            other_moves = []
            for i in range(len(best_move_list)):
                if best_move_list[i][0] > best_sum:
                    best_sum = best_move_list[i][0]
                    best_move = best_move_list[i][1]
                    best_length = best_move_list[i][2]
            if best_move == first:
                similar_moves = []
                for i in range(len(best_move_list)):
                    if best_move_list[i][0] == best_sum and best_move_list[i][2] < best_length:
                        best_length = best_move_list[i][2]
                for i in range(len(best_move_list)):
                    if best_move_list[i][0] == best_sum and best_move_list[i][2] == best_length:
                        similar_moves.append(best_move_list[i][1])
                    if best_move_list[i][0] == best_sum:
                        other_moves.append(best_move_list[i][1])
                is_there_a_pawn = []
                for i in range(len(similar_moves)):
                    if 'pawn' in tempboards[similar_moves[i][0]].name:
                        is_there_a_pawn.append(similar_moves[i])

                if len(is_there_a_pawn) > 0 and self.became_queen is False and self.count > 27:
                    best_move = random.choice(is_there_a_pawn)
                    self.last_move = best_move
                else:
                    self.last_move = ()
                    if self.count <= 10:
                        for i in range(len(similar_moves)):
                            if 'pawn' == self.board[similar_moves[i][0]].name:
                                if self.color == "white":
                                    if f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) - 1)}' in self.board and "queen" == self.board[f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) - 1)}'].name or f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) - 1)}' in self.board and "princess" == self.board[f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) - 1)}'].name:
                                        best_move = similar_moves[i]
                                if self.color == "black":
                                    if f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) + 1)}' in self.board and "queen" == self.board[f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) + 1)}'].name or f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) + 1)}' in self.board and "princess" == self.board[f'{similar_moves[i][0][0]}{(int(similar_moves[i][0][1]) + 1)}'].name:
                                        best_move = similar_moves[i]
                                return best_move
                    best_move = random.choice(similar_moves)
                    tempboards.make_move(best_move[0], best_move[1])
                    if tempboards.is_king_in_check(oppcolor):
                        self.see = self.see + 1
                    if self.see >= 7:
                        best_move = random.choice(other_moves)
            return best_move

    def get_total_score(self, temp_board, color):
        rook = 300
        bishop = 225
        queen = 500
        king = 5000
        pawn = 50
        knight = 150
        fool = 150
        princess = 375

        total_score = 0
        list = [str(i[1]) for i in temp_board.items() if color in str(i[1])]
        
        for i in range(len(list)):
            if "rook" in list[i]:
                total_score = total_score + rook
            if "knight" in list[i]:
                total_score = total_score + knight
            if "bishop" in list[i]:
                total_score = total_score + bishop
            if "queen" in list[i]:
                total_score = total_score + queen
            if "king" in list[i]:
                total_score = total_score + king
            if "pawn" in list[i]:
                total_score = total_score + pawn
            if "fool" in list[i]:
                total_score = total_score + fool
            if "princess" in list[i]:
                total_score = total_score + princess

        return total_score
