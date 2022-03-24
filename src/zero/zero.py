import random
from sklearn.neural_network import MLPClassifier
import sklearn
from copy import deepcopy
import numpy as np
import pandas as pd
class Game:
    def __init__(self,):
        self.state = [0,0,0,0, 1]
        self.action_space = [0,1,2,3]
    def reset(self,):
        self.state = [0,0,0,0, 1]
        self.action_space = [0,1,2,3]
        return self
    def play(self, action):
        """Reward: 0 (no outcome), 1 (player win), -1 player lose or illegal"""
        player = self.state[4]
        prev_state = self.state.copy()
        self.state[4] *= -1
        if self.state[action]!=0:
            reward = -1
        else:
            self.state[action] = player
            # specific
            if abs(sum(self.state[0:2]))==2*player or abs(sum(self.state[1:3]))==2*player or abs(sum(self.state[2:4]))==2*player:
                reward = player
            else:
                reward = 0
        return prev_state, self.state.copy(), reward, player
    
class Buffer:
    """History of plays. Doing the preprocessing here?"""
    def __init__(self,):
        self.all_time_buffer = []
        self.current_buffer = []
    def add_to_buffer(self, prev_state, state, reward, player, action, game):
        buffer_entry = (prev_state, state, reward, player, action, game)
        self.all_time_buffer.append(buffer_entry)
        
    def processed_buffer(self, player=None):
        """For now we consider only winning states for player"""
        buffer_df = pd.DataFrame(self.all_time_buffer, columns=["prev_state", "state", "reward", "player", "action", "n_game"])
        # taking only the actions of the games were player 1 is winning
        winning_buffer_df = pd.DataFrame()
        for player in [1, -1]:
            mask_winning = (buffer_df.reward==1) & (buffer_df.player==player)
            n_games_win = buffer_df[mask_winning].n_game.unique()
            winning_buffer_df_by_player = buffer_df[(buffer_df.n_game.isin(n_games_win)) & (buffer_df.player==player)]
            winning_buffer_df = pd.concat([winning_buffer_df, winning_buffer_df_by_player])
        
        winning_states = np.array([state for state in winning_buffer_df.prev_state])
        winning_actions = np.array([[action] for action in winning_buffer_df.action])
        return winning_states, winning_actions, n_games_win
        #self.current_buffer.append(buffer_entry)
        
class Model:
    def __init__(self, action_space, state):
        self.action_space = action_space
        self.state = state
        self.model = MLPClassifier(hidden_layer_sizes=(10,10))
        self.is_fitted = False
        
    def train(self, states, actions):

        self.model.fit(X=states, y=actions)           
        self.is_fitted = True
        
    
    def predict_action(self, state):
        if self.is_fitted:
            return self.model.predict(state.reshape(1,-1))[0]
        else:
            return random.choice(self.action_space)
class Simulation:
    """Simulation based on n games, player 1, player 2, ratio of model pred vs random and output processed buffer"""
    def simulate(self,model1, model2, n_games, ratio_random, game):
        buffer = Buffer()
        
        for n in range(n_games):
            game = game.reset()
            state = game.state.copy()
            while True:
                action = model1.predict_action(np.array(state))
                prev_state, state, reward, player = game.play(action=action)
                buffer.add_to_buffer(prev_state, state, reward, player, action, n)
                if reward !=0:
                    break
                action_2 = model2.predict_action(np.array(state))
                prev_state, state, reward_2, player_2 = game.play(action=action_2)
                buffer.add_to_buffer(prev_state, state, reward_2, player_2, action_2, n)
                if reward_2 !=0:
                    break
            
        return buffer
        
class Zero:
    """Model 1 vs model 2"""
    def __init__(self,):
        self.model_ini = Model(action_space=[0,1,2,3], state=[0,0,0,0])
    
    
    def run_once(self, model1, model2):
        simulation = Simulation()
        buffer = simulation.simulate(model1=model1, model2=model2, n_games=10000, ratio_random=0, game=Game())
        return buffer
    
    def run(self):
        # main model is model 1
        main_model = deepcopy(self.model_ini)
        #adv_model = deepcopy(self.model_ini)
        for n in range(5):
            print("n", n)
            #if n%2==0:
            #    print("for model 1")
            buffer = self.run_once(main_model, main_model)
            #    player=1
            #else:
            #    print("for model 2")
            #    buffer = self.run_once(adv_model, main_model)
            #    player = -1

            X, y, n_games_win = buffer.processed_buffer() 

            print("training")
            #adv_model = deepcopy(main_model)
            main_model.train(X, y)

zero = Zero()
buffer = zero.run()
print(buffer.all_time_buffer)
                