from typing import List, Tuple, Any, overload, Literal
from collections import OrderedDict, namedtuple
from itertools import product
from neuralogic.nn.neuron import Neuron, Node, OutputNeuron

class LogicGate(Node):
    r'''
    Logic Gate
    ---
    Directional weighted graph of McCulloch-Pitts Neurons
    capable to simulate all logic gates.

    Attributes:
    - numvars: int (default=2)
    number of variables that contains the LogicGate.
    - outputn: OutputNeuron (default=None)
    the last neuron of the network.
    - neurons: list (default=[])
    a list containing all neurons in the network.
    - inputs: list (default=[])
    a list of Node intances, one for each variable.
    - combinations: int (default=2**self.numvars)
    number of combinations of inputs. 
    - structure: dict (default={})
    the graph network structure.
    '''
    def __init__(
        self,
        numvars:int = 2
    ):
        self.numvars = numvars
        self.combinations = 2**self.numvars
        self.outputn: OutputNeuron = None
        self.neurons: List[Neuron] = []
        self.inputs = []
        self.insertInputs()
        self.structure = {}

    def __repr__(self) -> str:
        s = f'LogicGate(\n    {len(self.neurons)} neurons,'
        s += f'\n    {self.numvars} variables,'
        s += f'\n    Inputs = {str(self.inputs)}\n)'
        return s
    
    def insertInputs(self) -> List[Node]:
        r'''
        Called in the initialization of any LogicGate instance.

        Inplace method that compute ``self.inputs``, ``self.combinations`` and ``self.numvars``.
        The first one being a List with ``self.numvars`` Nodes, one for each
        variable containing a list of all the values for its variable
        in each combination.

        This method uses the built-in function ``product()`` from ``itertools`` library for the 
        creation of all inputs.

        Note that the output of each node is a list with equal size
        to the number of combinations.
        '''
        binary = [1,0]
        inputs = list(product(binary,repeat=self.numvars))
        self.inputs = [Node(out=[i[j] for i in inputs], key=j, isinput=True) for j in range(self.numvars)]
        self.combinations = len(inputs)

    def add(self, n):
        r'''
        Adds a non-connected neuron to the logic gate.

        If it's an instance of OutputNeuron, the method assigns ``self.outputn`` to the
        neuron. 
        '''
        if isinstance(n, Neuron):
            self.neurons.append(n)
            self.structure[n] = {}
            if isinstance(n, OutputNeuron) or n.isoutput:
                assert self.outputn == None, 'Can only exists one instance of OutputNeuron at the same LogicGate'
                self.outputn = n
                self.structure[n] = {}

    def merge(self, *args:List):
        r'''
        Inplace method that connects as instances of LogicGate as the number of variables
        that accepts the main LogicGate. The weights of the connexions are fixed and saved
        in ``n.weigths`` for each neuron.

        Its operation is basically clean the inputs of the receptive LogicGate and connect
        each neuron that in the first layer with the OutputNeuron of each ``*args`` LogicGate.

        Example - XOR building:
        ```python
        def XOR() -> LogicGate:
            FINAL = AND()
            OR_ = OR()
            NAND_ = NAND()
            FINAL.merge(OR_, NAND_)
            return FINAL
        ```

        It's useful in any creation of non-basic logic gates.
        '''
        assert len(args) == self.numvars, \
            f'This instance of {self.__class__} requires {self.combinations} \
                arguments but {len(args)} were given'
        
        for n in self.neurons:
            if n.firstlayer:
                n.inputs = []
                for idx,lg in enumerate(args):
                    if isinstance(lg, LogicGate):
                        self.connect(n1=lg.outputn, n2=n, w=n.weights[idx])
                    elif isinstance(lg, Node):
                        self.connect(n1=lg, n2=n, w=n.weights[idx])
        for lg in args:
            if isinstance(lg, LogicGate):
                self.neurons += lg.neurons

        self.combinations = max([self.combinations]+[arg.combinations if isinstance(arg,LogicGate) else len(arg.out) for arg in args])
        
    def connect(self, n1, n2, w):
        r'''
        Adds a weigthed connection between neuron 1 and 2
        '''
        assert isinstance(n2,Neuron), 'n2 must be an instance of Neuron.'
        if isinstance(n1,Node):
            #self.structure[n2].append(n1)
            n2.inputs.append(n1)
            n2.weights.append(w)
        else:
            raise TypeError('n1 must be an instance of Node.')
    
    def predict(self) -> Literal[0, 1]:
        r'''
        Executes the network and returns the results for all tuples in inputs

        It works calling the ``compute()`` method of ``self.outputn``, which calls
        recursively the ``compute()`` method of each Node in the network.

        The final result is saved in self.out.
        '''
        self.out = []
        for i in range(self.combinations):
            self.outputn.compute(it=i)
            self.out.append(self.outputn.out)
        return self.out

class UnaryLG(LogicGate):
    pass

class BinaryLG(LogicGate):
    pass
