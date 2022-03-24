import random

import numpy as np
import pandas as pd
from src.drl.game import Game


class RLAgent:
    """Representation of the agent that will play the game"""
    def __init__(self, model, game, ratio_explotation_exploration):
        self.model = model
        self.model_is_fitted = False
        self.game = game
        self.columns = [f"s_{x}" for x in range(len(self.game.action_space))]
        self.cont = 0
        self.ratio_explotation_exploration = ratio_explotation_exploration
        
    def choose_action(self, actions, list_states, player, force_model_prediction=False):
        """Choose action from current possible actions """
        if ((self.model_is_fitted) and ((self.cont % self.ratio_explotation_exploration) != 0)) or force_model_prediction :
            if player==-1:
                list_states = [invert_state(list_1) for list_1 in list_states]
            model_action_max=np.argmax(self.model.predict(pd.DataFrame(list_states, columns=self.columns)))
            action = actions[model_action_max]
        else:
            action = random.choice(actions)
            
        self.cont+=1
        return action
        
class RLSimulation:
    """Representation of the game simulation"""
    def __init__(
         self,
         n_games: int,
         game: Game,
         agent: RLAgent
    ):
        self.n_games = n_games
        self.game = game
        self.agent = agent
        
    def run_simulations(self,):
        processed_buffer=[]
        for _ in range(self.n_games):
            buffer = self.run()
            processed_buffer.append(self.process_buffer(buffer))
            
        return processed_buffer
        
    def run(self,):
        """Run one game and return outcome and buffer from the game (history of states)"""
        self.game.reset()
        buffer_one_game = []
        while True:
            actions = self.game._get_possible_actions(state=self.game.board)
            next_states_list = self.game._get_possible_next_states(state=self.game.board)
            action = self.agent.choose_action(actions, next_states_list, player=self.game.player)
            outcome = self.game.play(action=action)

            # the game player is inverted because once the movement is done, the player change
            buffer_one_game.append((action, self.game.board, outcome, -self.game.player))
            if outcome is not None:
                break
        return buffer_one_game
    
    def process_buffer(self, buffer: list):
        """ We want to process the buffer from one game. How? Give the reward to player that ended 
        the game and invert the state since we will consider the model only from the perspective of the player one"""

        # TODO: there must be a simplest way of doing it
        last_action, last_state, last_reward, last_player = buffer[-1]
        if last_reward == 0.5:
            # reward is value
            buffer_processed = [(state, last_reward) if player==1 else (invert_state(state), last_reward) for (action, state, value, player) in buffer  ]

        elif last_reward == 1 and last_player==1:
            buffer_processed = [(state, last_reward) if player==1 else (invert_state(state), 1-last_reward) for (action, state, value, player) in buffer  ]

        elif last_reward == 1 and last_player==-1:
            buffer_processed = [(state, 1-last_reward) if player==1 else (invert_state(state), last_reward) for (action, state, value, player) in buffer  ]

        else:
            raise ValueError("something went wrong in buffer processing")
            
        return buffer_processed
            
        
        
class Trainer:
    """Representation of training"""
    def __init__(self, n_simulations: int, sim: RLSimulation):
        self.n_simulations = n_simulations
        self.sim = sim
        self.training_buffer = pd.DataFrame()
        self.all_buffer = pd.DataFrame()
        self.score=[]
    def main(self):
        for it in range(self.n_simulations):
            print(f"training step: {it}/{self.n_simulations}")
            self.training_buffer = self.from_buffer_to_df(self.sim.run_simulations())
            self.train(it)
            self.update_all_buffer()
            self.evaluate()
    def train(self):

        self.sim.agent.model.fit(X=self.training_buffer[self.sim.agent.columns], y=self.training_buffer["value"])
        if not self.sim.agent.model_is_fitted:
            self.sim.agent.model_is_fitted = True
            
    def evaluate(self,):
        score = self.sim.agent.model.score(X=self.all_buffer[self.sim.agent.columns],y=self.all_buffer["value"])
        #print(score)
        self.score.append(score)
            
    def from_buffer_to_df(self,buffer):
        buffer = [state for buffer_ind in buffer for state in buffer_ind  ]
        buffer_df=pd.DataFrame(buffer, columns=["state", "value"])
        buffer_df[self.sim.agent.columns] = pd.DataFrame(buffer_df.state.tolist(), index = buffer_df.index)
        return buffer_df
    
    def update_all_buffer(self):
        self.all_buffer = pd.concat([self.all_buffer, self.training_buffer])

def invert_state(state):
    """From the perspective of player 1"""
    state=[-x for x in state]
    return state