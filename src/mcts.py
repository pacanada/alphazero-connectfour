from game import Game
from node import Node
import numpy as np
import random
import copy
def UCB(w, n, N, c=2):
    """
    w number of wins, n number of runs of the node, 
    N total number of simulations of the parent node, c exploration parameter
    """
    out = w/n*c*(math.log(N)/n)**(0.5)
    
def invert_state(state: list):
    """From the perspective of player 1"""
    if sum(np.array(state))!=0:
        state=[-x for x in state]
    return state
    
class MonteCarloTreeSearch:
    """Always from the perspective of one player
    Start in state0 s0
        is a leaf node?
            no: select child that maximize UCB as current state (repeat)
            yes:
            
    """
    def __init__(self, game: Game, number_simulations=4):
        self.game = game
        self.number_simulations=number_simulations

    def run(self, root_state):
        """Main loop"""
        root = Node(state=root_state, is_root=True, is_leaf=True)
        for n in range(self.number_simulations):
            node = root
            if node.is_leaf and len(node.children)==0:
                if node.visits==0:
                    # rollout
                    outcome = self.rollout(state=node.state)
                    # update node
                    node = self.update_node_based_on_outcome(outcome=outcome, node=node)

                else:
                    print("here")
                    # for each available action add children and run rollout
                    possible_next_states = self.game._get_possible_next_states(state=node.state)
                    for next_state in possible_next_states:
                        node.add_children(state_children=next_state)
                    #root = node.children[0]
                    ## rollout
                    #outcome = self.rollout(state=node.state)
                    ## update node
                    #node = self.update_node_based_on_outcome(outcome=outcome, node=node)
            else:
                
                print("here 2")
        
        return node
    
    def rollout(self,state):
        """Monte Carlo simulation for the state"""
        
        self.game = copy.deepcopy(self.game.init_custom(state=invert_state(state), player=1))
        while True:
            
            random_action = random.choice(self.game._get_possible_actions(state=self.game.board))
            outcome = self.game.play_mcts(action=random_action)
            ## the outcome is the reward values (1 for winning, 0.5 draw, 0 lose and None while playing)
            if outcome is not None:
                break

        return outcome
    def update_node_based_on_outcome(self, outcome: float, node: Node):
        """For now we only consider winning, not draw"""
        if outcome == self.game.reward_win:
            node=node.update_node(wins=1, visits=1)
        else:
            node=node.update_node(wins=0, visits=1)
            
        return node
        
    
        

        
