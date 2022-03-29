import json
import random
import numpy as np

list_index_win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

def get_reward(state):
    for win_combination in list_index_win:
        if sum(state[win_combination]) == 3: 
            return 1
        elif sum(state[win_combination]) == -3:
            return -1
        elif len(np.where(state==0)[0]) == 0:
            # Draw
            return 0
    return None

def get_children(state, player):
    children = []
    available_positions = np.where(state==0)[0]
    for position in available_positions:
        new_state = state.copy()
        new_state[position] = player
        children.append(Node(new_state, -player))
    return children
class Node:
    def __init__(self, state, player):
        self.state = state
        self.player = player
        self.reward = get_reward(state)
        self.children = [] if self.reward else get_children(state, player)
    def __repr__(self):
        return f"State:{self.state}, player {self.player}, reward {self.reward}"


# recursion
def minimax(node:Node, depth, maximize):
    if depth ==0 or len(node.children)==0:
        return node.reward
    if maximize:
        maxeva=-float("inf")
        for children in node.children:
            eva = minimax(children, depth-1, False)
            maxeva = max(eva, maxeva)
        return maxeva
    else:
        mineva=+float("inf")
        for children in node.children:
            eva = minimax(children, depth-1, True)
            mineva = min(eva, mineva)

        return mineva
    
class TicTacToePlayer:
    def __init__(self, state, player):
        self.tree = Node(state, player)
    def choose_best(self):
        """Takes a lot of time in initial board states"""
        minimax_scores = []
        for children in self.tree.children:
            # maximize if player 1, minimize otherwise
            maximize = self.tree.player==1
            minimax_scores.append(minimax(children, 10, maximize))
        if maximize:
            # check position that is different
            pos = np.argwhere(self.tree.state != self.tree.children[np.argmax(minimax_scores)].state)[0][0]
            return pos, (self.tree.children[np.argmax(minimax_scores)], minimax_scores, self.tree.children)
        else:
            pos = np.argwhere(self.tree.state != self.tree.children[np.argmin(minimax_scores)].state)[0][0]
            return pos, (self.tree.children[np.argmin(minimax_scores)], minimax_scores, self.tree.children)

class TicTacToePlayerToJson:
    def __init__(self, state, player):
        self.tree = Node(state, player)
        self.state_dict = {}
        
    def minimax_save_dict(self, node, depth, maximize):
        """ Caching the minimax result in a dictionary """
        if depth ==0 or len(node.children)==0:
            self.state_dict[str(node.state)] = {"minimax": node.reward, "next": []}
            return node.reward
        if maximize:
            maxeva=-float("inf")
            for children in node.children:
                eva = self.minimax_save_dict(children, depth-1, False)
                maxeva = max(eva, maxeva)
            self.state_dict[str(node.state)] = {"minimax": maxeva, "next": [str(children.state) for children in node.children]}
            return maxeva
        else:
            mineva=+float("inf")
            for children in node.children:
                eva = self.minimax_save_dict(children, depth-1, True)
                mineva = min(eva, mineva)
            self.state_dict[str(node.state)] = {"minimax": mineva, "next": [str(children.state) for children in node.children]}

            return mineva

    def to_json(self, path="tictactoe_solver.json"):
        self.minimax_save_dict(self.tree, 10, True)
        with open(path, 'w') as outfile:
            json.dump(self.state_dict, outfile)


  
# Serialize dict with minimax result
#player = TicTacToePlayerToJson(np.array([0,0,0,0,0,0,0,0,0]), 1)
#player.to_json()
class TicTacToeLookUpSolver():
    """It uses a lookup table to find the best move based on the minimax algorithm. """
    def __init__(self, path):
        self.minimax_dict = self.load_minimax_dict(path)
        
    def load_minimax_dict(self, path):
        with open(path) as json_file:
            minimax_dict = json.load(json_file)
        return minimax_dict
        
    def convert_to_str(self, state):
        return str(np.array(state))
    
    def convert_str_to_position(self, state_string):
        return np.array(state_string.replace("[","").replace("]","").split(), dtype=int)
    
    def play(self, state, debug=False, difficulty=10):
        """Difficulty=10 is perfect play, difficulty = 0 it will make perfect play once every 10 moves"""
        state_str = self.convert_to_str(state)
        # Perfect play, the minimax value of the position would be the minimax value of the child
        candidates = [next_state for next_state in self.minimax_dict[state_str]["next"] if self.minimax_dict[self.convert_to_str(next_state)]["minimax"]==self.minimax_dict[state_str]["minimax"]]
        pos = [np.argwhere(state != self.convert_str_to_position(next_state))[0][0] for next_state in candidates]
        if debug:
            print("Candidates:", candidates)
            print("Minimax", self.minimax_dict[state_str]["minimax"])
        if random.randint(0,10-difficulty)==0:
            ret = random.choice(pos)

        else:

            ret = random.choice(np.argwhere(np.array(state)==0))[0]
            
        
        return ret

    
        
    