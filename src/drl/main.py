# 20,20  2 200 200 
from sklearn.neural_network import MLPRegressor
from src.drl.game import TicTacToe
from src.drl.zero import RLAgent, RLSimulation, Trainer


model = MLPRegressor(
            hidden_layer_sizes=(30,30),
            random_state=1, n_iter_no_change=10000, tol=1e-7,
            max_iter=100, verbose=False,
            warm_start=True)
game = TicTacToe()
agent = RLAgent(model=model, game=game, ratio_explotation_exploration=3)
sim = RLSimulation(n_games=100, game=game, agent= agent)
trainer = Trainer(n_simulations=500, sim=sim)

trainer.main()

import pickle
with open(f"tictactoe_trainer_5.pickle", "wb") as f:
    # avoid api key to be serialized
    pickle.dump(trainer, f)