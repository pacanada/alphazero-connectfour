from game import Connect2
from mcts import MonteCarloTreeSearch
mcts = MonteCarloTreeSearch(game=Connect2())
node=mcts.run(root_state=[0,0,0,0])
print(node)
print(node.children)
