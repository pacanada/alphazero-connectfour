from itertools import combinations, permutations, combinations_with_replacement, product
import itertools
import numpy as np
import random
import copy

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
    
class Connect2():
    def __init__(self, state:list=[0,0,0,0] ):
        self.board=state
        self.action_space=[0,1,2,3]
        self.player=1
        self.reward_win = 1
        self.reward_draw = 0.5
        self.reward_loss = 0
        
        
    def reset(self,):
        self.board=[0,0,0,0]
        self.player=1
        return self
    
    def init_custom(self,state, player):
        self.board=state
        self.player=player
        return self

    def play(self, action):
      
        if action not in self.action_space:
            raise ValueError(f"Action: {action} is not allowed from the action space: {self.action_space}")
            
        if self._is_legal(action):
            self.board[action]= self.player
            is_win=self._is_win()
            if is_win:
                print("player", self.player, "is winner")
                return self.reward_win
            if not is_win and len(self._get_possible_actions(self.board))==0:
                print("draw")
                return self.reward_draw
            
            self.player = self.player*-1
            
        else:
            raise ValueError("Illegal move")
            
    def play_mcts(self, action):
        """From the perspective of player 1"""
      
        if action not in self.action_space:
            raise ValueError(f"Action: {action} is not allowed from the action space: {self.action_space}")
            
        if self._is_legal(action):
            self.board[action]= self.player
            is_win=self._is_win()
            if is_win and self.player==1:
                print("player", self.player, "is winner")
                return self.reward_win
            elif is_win and self.player==-1:
                print("player", self.player, "is winner")
                return self.reward_loss
            elif not is_win and len(self._get_possible_actions(self.board))==0:
                print("draw")
                return self.reward_draw
            
            self.player = self.player*-1
            
        else:
            raise ValueError("Illegal move")
        
    def _is_legal(self, action, state=None):
        """We allow to ways of calling the method. Directly to check if an state is win or lost or by chcking the board"""
        is_legal=False
        
        if state is None:
            state = self.board.copy()

        if state[action]==0:
            is_legal=True
        return is_legal

    def _is_win(self, state=None):
        """We allow to ways of calling the method. Directly to check if an state is win or lost or by chcking the board"""
        is_win = False
        if state is None:
            state = self.board.copy()
            
        if abs(sum(state[0:2]))==2 or abs(sum(state[1:3]))==2 or abs(sum(state[2:4]))==2:
            #print(self.player, "is winner")
            is_win = True
            return is_win
        


    def _get_possible_next_states(self, state):
        """Give possible states from the state position. Action is the same as index. Potentially problematic.
        We are passing current state as argument, not necessarily the state of the board as it is."""
        possible_actions = self._get_possible_actions(state=state)
        possible_next_states = []
        
        for action in possible_actions:
            board = state.copy()
            board[action]=self.player
            possible_next_states.append(board)
            
        return possible_next_states

        
    def _get_possible_actions(self, state): 
        """Return all posible actions in the form of array [1,2] for example for [1,0,0,-1]"""
        return np.where(np.array(state)==0)[0]
    
        
    def render(self,):
        print(self.board, "Next player:", self.player)



