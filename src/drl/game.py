import numpy as np
from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def _is_legal(self):
        pass

    @abstractmethod
    def _is_win(self):
        pass

    @abstractmethod
    def _get_possible_next_states(self):
        pass


class TicTacToe():
    def __init__(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.action_space = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.player = 1
        self.reward_win = 1
        self.reward_draw = 0.5
        self.list_index_win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [
            0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def reset(self,):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.player = 1

    def _get_possible_next_states(self, state):
        """Give possible states from the state position. Action is the same as index. Potentially problematic.
        We are passing current state as argument, not necessarily the state of the board as it is."""
        possible_actions = self._get_possible_actions(state=state)
        possible_next_states = []

        for action in possible_actions:
            board = state.copy()
            board[action] = self.player
            possible_next_states.append(board)

        return possible_next_states

    def _get_possible_actions(self, state):
        """Return all posible actions in the form of array [1,2] for example for [1,0,0,-1]"""
        return np.where(np.array(state) == 0)[0]

    def render_table(self,):
        print(np.array(self.board).reshape(3, 3), "Next player:", self.player)

    def _is_legal(self, action, state=None):
        """We allow to ways of calling the method. Directly to check if an state is win or lost or by chcking the board"""
        is_legal = False

        if state is None:
            state = self.board.copy()

        if state[action] == 0:
            is_legal = True
        return is_legal

    def _is_win(self, state=None):
        """We allow to ways of calling the method. Directly to check if an state is win or lost or by chcking the board"""
        is_win = False
        if state is None:
            state = self.board.copy()
        state_array = np.array(state)
        for win_combination in self.list_index_win:
            if abs(sum(state_array[win_combination])) == 3:
                is_win = True
                return is_win

    def play(self, action):
        """From the perspective of player 1"""
        output = None
        if action not in self.action_space:
            raise ValueError(
                f"Action: {action} is not allowed from the action space: {self.action_space}")

        if self._is_legal(action):
            board_temp = self.board.copy()
            board_temp[action] = self.player
            self.board = board_temp.copy()
            is_win = self._is_win()
            if is_win:
                output = self.reward_win
            elif not is_win and len(self._get_possible_actions(self.board)) == 0:
                output = self.reward_draw

            self.player = self.player*-1

        else:
            raise ValueError("Illegal move")
        return output
