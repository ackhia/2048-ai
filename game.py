# coding=utf-8

#Credit gose to wbars for this code
#Modified from: https://gist.github.com/wbars/88df9704306629c40c7929e691b48b98

import sys

import numpy as np
from numpy.random import choice
import copy

np.set_printoptions(suppress=True)

class Action:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def get_action(cls, keyboard_key):
        moves = {'w': Action.UP, 'd': Action.RIGHT, 's': Action.DOWN, 'a': Action.LEFT}
        if keyboard_key not in moves:
            raise Exception
        return moves[keyboard_key]


def stack(board):
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            k = i
            while board[k][j] == 0:
                if k == len(board) - 1:
                    break
                k += 1
            if k != i:
                board[i][j], board[k][j] = board[k][j], 0


def sum_up(board):
    for i in range(0, len(board) - 1):
        for j in range(0, len(board)):
            if board[i][j] != 0 and board[i][j] == board[i + 1][j]:
                board[i][j] += board[i + 1][j]
                board[i + 1][j] = 0


class Board:
    def __init__(self, size):
        self.__board = np.zeros((size, size))
        self.__score = 0
        self.drop_elem()

    def completed(self):
        if len(np.where(self.__board == 0)[0]) == 0:
            self_copy = copy.deepcopy(self)

            if(self_copy.move(Action.UP) == False 
            and self_copy.move(Action.DOWN) == False 
            and self_copy.move(Action.LEFT) == False 
            and self_copy.move(Action.RIGHT) == False):
                return True
        return False


    def move(self, action):
        #self.paint()
        board_copy = copy.deepcopy(self.__board)
        rotated_board = np.rot90(board_copy, action)
        stack(rotated_board)
        sum_up(rotated_board)
        stack(rotated_board)
        new_board = np.rot90(rotated_board, len(self.__board) - action)

        moved = False
        if not (new_board == self.__board).all():
            self.__board = new_board
            self.drop_elem()
            moved = True

        self.calculate_score()

        return moved


    def calculate_score(self):
        self.__score = np.max(self.__board)

    def paint(self):
        print(np.array_str(self.__board, 120, 0))

    def score(self):
        return self.__score

    def average_score(self):
        return np.nanmean(np.where(self.__board!=0,self.__board,np.nan))

    def drop_elem(self):
        elem = choice([2, len(self.__board)], 1, False, [0.9, 0.1])[0]
        zeroes_flatten = np.where(self.__board == 0)
        zeroes_indices = [(x, y) for x, y in zip(zeroes_flatten[0], zeroes_flatten[1])]
        random_index = zeroes_indices[choice(len(zeroes_indices), 1)[0]]
        self.__board[random_index] = elem


def run():
    board = Board(4)
    while True:
        moved = board.move(Action.get_action(input("Next move?\n")))
        board.paint()
        if board.completed():
            break
        print("Score: " + str(board.score()))
        print("moved", moved)


if __name__ == '__main__':
    sys.exit(run())
