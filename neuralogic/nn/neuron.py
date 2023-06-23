from typing import List, Tuple, Literal

class Node:
    def __init__(
        self, 
        key:int = None, 
        out:int|List = None,
        isinput:bool = False
    ) -> None:
        self.key = key
        self.out = out
        self.isinput = isinput
        if self.isinput and not isinstance(self.out, List):
            raise TypeError('Output must be a list of input values for the LogicGate')
    
    def __repr__(self) -> str:
        s = f'Node(out={self.out})'
        return s

class Neuron(Node):
    def __init__(
        self, 
        tau:int, 
        firstlayer:bool = False
    ) -> None:
        super().__init__()
        self.tau = tau
        self.inputs:List[Node] = []
        self.weigths:List[int] = []
        self.firstlayer = firstlayer
    
    def __repr__(self) -> str:
        s = f'Neuron(out={self.out},tau={self.tau})'
        return s

    def compute(self,it) -> Literal[0, 1]:
        for n in self.inputs:
            if not n.isinput:
                n.compute(it=it)
        self.out = 1 if sum([v.out[it]*w if v.isinput else v.out*w for v,w in zip(self.inputs,self.weigths)]) >= self.tau else 0
        return self.out

class OutputNeuron(Neuron):
    '''
    Abstract class refering to the unique output neuron.
    '''
    def __init__(self, tau: int, firstlayer:bool) -> None:
        super().__init__(tau, firstlayer)