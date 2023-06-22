from typing import List, Tuple, Literal

class Node:
    def __init__(
        self, 
        key:int = None, 
        out:int|List = None,
        input:bool = False
    ) -> None:
        self.key = key
        self.out = out
        self.input = input
        if self.input and not isinstance(self.out, List):
            raise TypeError
    
    def __repr__(self) -> str:
        s = f'Node(out={self.out})'
        return s

class Neuron(Node):
    def __init__(self, tau:int) -> None:
        super().__init__()
        self.tau = tau
        self.inputs:List[Tuple[Neuron,int]] = []
    
    def __repr__(self) -> str:
        s = f'Neuron({self.key},tau={self.tau})'
        return s

    def compute(self,it) -> Literal[0, 1]:
        for n,w in self.inputs:
            if not n.input:
                n.compute(it=it)
        self.out = 1 if sum([v.out[it]*w if v.input else v.out*w for v,w in self.inputs]) >= self.tau else 0
        return self.out

class OutputNeuron(Neuron):
    '''
    Abstract class refering to the unique output neuron.
    '''
    def __init__(self, tau: int) -> None:
        super().__init__(tau)