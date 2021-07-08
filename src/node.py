class Node:
    def __init__(self, state: list=None, parent=None, is_root=False, is_leaf=False, path_to_root=None):
        self.state = state
        self.is_root = is_root
        self.parent = parent
        self.is_leaf = is_leaf
        self.children = []
        self.ucp=0
        self.wins=0
        self.visits=0
        self.path_to_root=path_to_root
        
    def __repr__(self):
        return f"State:{self.state}, is_root={self.is_root},is_leaf={self.is_leaf}\n Visits:{self.visits}, Wins: {self.wins} \n" + f"children:{[children_node.state for children_node in self.children]}"
        
    def add_children(self, state_children):
        #path_to_root = [self.path_to_root,key_state]
        #key = str(state_children)
        self.children.append(Node(state=state_children, is_root=False, is_leaf=True))#, path_to_root=path_to_root))
        self.is_leaf=False
        
    def update_node(self, wins, visits):
        self.wins+=wins
        self.visits+=visits
        return self