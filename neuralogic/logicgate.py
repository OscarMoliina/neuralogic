from typing import List, Tuple, Any, overload, Literal
from collections import OrderedDict, namedtuple
from itertools import product
from neuralogic.nn.neuron import Neuron, Node, OutputNeuron

class LogicGate(Node):
    '''
    Logic Gate: Directional weighted graph of Neurons
    '''
    def __init__(
        self,
        variables:int = 2
    ):
        self.outputn: OutputNeuron = None
        self.neurons = []
        self.combinations = None
        self.variables = variables #inputsize
        self.insertInputs()
        self.structure = {tpl:[] for tpl in self.inputs}

    def __repr__(self) -> str:
        s = f'LogicGate(\n    {len(self.neurons)} neurons,'
        s += f'\n    Structure = {str(self.structure)}\n)'
        return s
    
    def insertInputs(self) -> List[Node]:
        '''
        Inplace method that compute self.inputs, self.combinations and self.variables.
        The first one being a List with self.variables Nodes, one for each
        variable containing a list of all the values for its variable
        in each combination.

        Note that the output of each node is a list with length equal
        to the number of combinations.
        '''
        binary = [0,1]
        inputs = list(product(binary,repeat=self.variables))
        self.inputs = [Node(out=[i[j] for i in inputs], isinput=True) for j in range(len(inputs[0]))]
        self.combinations = len(inputs)

    def add(self, n):
        '''
        Adds a non-connected neuron to the logic gate.
        '''
        if isinstance(n, Neuron) and not isinstance(n, OutputNeuron):
            self.neurons.append(n)
            self.structure[n] = []
        elif isinstance(n, OutputNeuron):
            assert self.outputn == None, 'Can only exists one instance of OutputNeuron at the same LogicGate'
            self.outputn = n
            self.neurons.append(n)
            self.structure[n] = []

    def merge(self, *args:List):
        '''
        Combines 2 instances of LogicGate
        '''
        assert len(args) == self.variables, \
            f'This instance of {self.__class__} requires {self.combinations} \
                arguments but {len(args)} were given'
        
        for n in self.neurons:
            if n.firstlayer:
                n.inputs = []
                for idx,lg in enumerate(args):
                    self.connect(n1=lg.outputn, n2=n, w=n.weigths[idx])
        
        self.combinations = max([self.combinations]+[arg.combinations for arg in args])
        
    def connect(self, n1, n2, w):
        '''
        Adds a weigthed connection between neuron 1 and 2
        '''
        assert isinstance(n2,Neuron), 'n2 must be an instance of Neuron.'
        if isinstance(n1,Node) or isinstance(n1,Neuron):
            self.structure[n2].append(n1)
            n2.inputs.append(n1)
            n2.weigths.append(w)
        else:
            raise TypeError
    
    def predict(self) -> Literal[0, 1]:
        '''
        Executes the network and returns the results for all tuples in inputs
        The final result is saved in self.out.
        '''
        self.out = []
        for i in range(self.combinations):
            self.outputn.compute(it=i)
            self.out.append(self.outputn.out)
        return self.out