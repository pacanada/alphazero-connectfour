import numpy as np

list_index_win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

class Node:
    def __init__(self, state, player):
        self.state = state
        self.player = player
        self.children = self.get_children(state)
    def __repr__(self):
        return f"State:{self.state}, player {self.player}, reward {self.reward}"
    def get_children(self, state):
        children = []
        available_positions = np.where(state==0)[0]
        self.reward = self.get_reward()
        if self.reward:
            # empty children
            pass
        elif len(available_positions)==0 and self.reward is None:
            self.reward = 0
        else: 
            for position in available_positions:
                new_state = state.copy()
                new_state[position] = self.player
                children.append(Node(new_state, -self.player))
        return children
                
    def get_reward(self):
        for win_combination in list_index_win:
            if sum(self.state[win_combination]) == 3: #*self.player:
                return 1
            elif sum(self.state[win_combination]) == -3: #*self.player:
                return -1
        return None

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
                
# example                   
player = TicTacToePlayer(np.array([1,0,0,0,0,0,0,0,0]), -1)
player.choose_best()  
    
        
    