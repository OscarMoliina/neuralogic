from typing import List, Tuple, Literal

class Node:
    r'''
    Node
    ---
    Abstract class which englobes all the elements in the network.

    Attributes:
    - out: int|list (default=None)
    output number (or list) of the node. It'll be list of numbers
    if the instance represents an input node of the network.
    - isinput: bool (default=False) 
    True when the the instance represents an input node of the network.
    '''
    def __init__(
        self, 
        key:int|str = None, 
        out:int|List = None,
        isinput:bool = False
    ) -> None:
        self.key = key
        self.out = out
        self.isinput = isinput
        if self.isinput and not isinstance(self.out, List):
            raise TypeError('Output must be a list of input values for the LogicGate')
    
    def __repr__(self) -> str:
        s = f'Node(out={self.out},key={self.key})'
        return s
    
    def __eq__(self, __value: object) -> bool:
        return self.key == __value.key
    
    def __hash__(self) -> int:
        return hash(self.key)

    def copy(self) -> 'Node':
        return Node(
            key=self.key, 
            out=self.out.copy(),
            isinput=self.isinput
        )

class Neuron(Node):
    r'''
    Neuron
    ---
    Class representing a McCulloch-Pitts Perceptron. 
    It inherits from Node.

    Attributes:
    - tau: int (default=0)
    this number is the limit to decide the output of the neuron
    given a list of inputs and weigths.
    - inputs: list (default=[])
    list of nodes from which its output is taken as input for the neuron.
    - weights: list (default=[])
    list of weights which connects each input to the neuron.
    - firstlayer: bool (default=False)
    True if the neuron belong to the first layer of the LogicGate.
    '''
    def __init__(
        self, 
        key:int|str = None, 
        out:int|List = None,
        isinput:bool = False,
        tau:int = 0, 
        weights:List[int] = None,
        firstlayer:bool = False,
        isoutput:bool = False
    ) -> None:
        super().__init__(key=key, out=out, isinput=isinput)
        self.tau = tau
        self.inputs:List[Node] = []
        self.weights:List[int] = [] if weights == None else weights
        self.firstlayer = firstlayer
        self.isoutput = isoutput
    
    def __repr__(self) -> str:
        s = f'Neuron(out={self.out},key={self.key},tau={self.tau},weights={self.weights})'
        return s
    
    def connect(self, node:Node, w:int) -> None:
        r'''
        Adds a weigthed connection between the instance Neuron and the
        argument Node.
        '''
        assert isinstance(node, Node)
        self.inputs.append(node)
        self.weights.append(w)
        
        return None

    def compute(self,it) -> Literal[0, 1]:
        r'''
        Method which computes the output of the neuron.

        .. math::
        \[
        \textbf{function: } 
        \begin{cases}
            1, & \text{if } \sum_{i=1}^{\text{len(inputs)}} x_i w_i \geq \tau \\
            0, & \text{else}
        \end{cases}
        \]
        '''
        for n in self.inputs:
            if not n.isinput:
                n.compute(it=it)
        self.out = 1 if sum([n.out[it]*w if n.isinput else n.out*w for n,w in zip(self.inputs,self.weights)]) >= self.tau else 0
        return self.out
