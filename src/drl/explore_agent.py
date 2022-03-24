import pickle
from src.drl.game import TicTacToe
from src.drl.zero import Trainer, RLSimulation, RLAgent
def get_action(game, agent):
    actions = game._get_possible_actions(state=game.board)
    next_states_list = game._get_possible_next_states(state=game.board)
    action = agent.choose_action(actions, next_states_list, player=game.player, force_model_prediction=True)
    return action

with open("tictactoe_trainer_5.pickle", "rb") as f:
    trainer = pickle.load(f)

game=TicTacToe()
game.reset()
while True:
    input_player_1 = int(input("your action"))
    game.play(input_player_1)
    game.render_table()
    game.play(get_action(game, trainer.sim.agent))
    game.render_table()