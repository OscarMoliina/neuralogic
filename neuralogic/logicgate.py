from typing import List, Tuple, Any, overload, Literal
from collections import OrderedDict, namedtuple
from neuralogic.nn.neuron import Neuron, Node, OutputNeuron

class LogicGate(Node):
    '''
    Logic Gate: Directional weighted graph of Neurons
    '''
    def __init__(
        self, 
        neurons:List[Neuron] = [], 
        inputs:List = []
    ):
        self.outputn: OutputNeuron = None
        self.neurons = neurons
        self.inputs  = self.toNode(inputs)
        self.inplength = len(self.inputs[0].out)
        self.structure = {tpl:[] for tpl in self.inputs}

    def __repr__(self) -> str:
        s = f'LogicGate(\n    {len(self.neurons)} neurons,'
        s += f'\n    Structure = {str(self.structure)}\n)'
        return s
    
    def toNode(self, inputs):
        return [
            Node(out=[i[0] for i in inputs], input=True),
            Node(out=[i[1] for i in inputs], input=True)
        ]

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

    def merge(self,other):
        '''
        TODO: Combines 2 instances of LogicGate
        '''

    def connect(self, n1, n2, w):
        '''
        Adds a weigthed connection between neuron 1 and 2
        '''
        assert isinstance(n2,Neuron), 'n2 must be an instance of Neuron.'
        if isinstance(n1,Node) or isinstance(n1,Neuron):
            self.structure[n2].append(n1)
            n2.inputs.append((n1,w))
        else:
            raise TypeError
    
    def predict(self) -> Literal[0, 1]:
        '''
        Executes the network and returns the results for all tuples in inputs
        The final result is saved in self.out.
        '''
        self.out = []
        for i in range(self.inplength):
            self.outputn.out = self.outputn.compute(it=i)
            self.out.append(self.outputn.out)
        return self.out