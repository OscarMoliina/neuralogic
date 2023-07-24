from typing import List, Tuple, Any, overload, Literal, Set
from collections import OrderedDict, namedtuple
from itertools import product
from neuralogic.nn.neuron import Neuron, Node

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
        self.outputn: Neuron = None
        self.neurons: List[Neuron] = []
        self.inputs: List[Node] = [] 
        self.variables:OrderedDict[int:List] = OrderedDict()
        self.insertInputs()

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
        self.inputs = [Node(out=[i[j] for i in inputs], key=chr(65+j), isinput=True) for j in range(self.numvars)]
        for inp in self.inputs:
            self.variables[inp.key] = inp.out

    def add(self, *neurons:'Neuron'):
        r'''
        Adds a non-connected neuron to the logic gate.

        If it's an instance of OutputNeuron, the method assigns ``self.outputn`` to the
        neuron. 
        '''
        for n in neurons:
            if isinstance(n, Neuron):
                self.neurons.append(n)
                if n.isoutput and not self.outputn:
                    self.outputn = n

    def merge(self, *args:'LogicGate'):
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
            f'This instance of {self.__class__} requires {self.numvars} \
                arguments but {len(args)} were given'
        
        aux_variables = self.variables.copy()
        aux_neurons = self.neurons.copy()
        self.variables = OrderedDict()
        self.inputs = []

        # Añadimos a variables los nuevos inputs y a neuronas las nuevas neuronas
        for lg in args:
            if isinstance(lg,LogicGate):
                for n in lg.neurons:
                    self.add(n)
                for inp in lg.inputs:
                    self.variables[inp.key] = None
                    self.inputs.append(inp.copy())
            elif isinstance(lg,Node):
                self.variables[lg.key] = None
                self.inputs.append(lg.copy())
        
        # Canviem els inp.out dels inputs
        self.numvars = len(self.variables)
        self.combinations = 2**self.numvars
        binary = [1,0]
        inputs = list(product(binary,repeat=self.numvars))
        
        for idx,key in enumerate(self.variables):
            self.variables[key] = [i[idx] for i in inputs]
        
        for node in self.inputs:
            node.out = self.variables[node.key]

        # Pas 1: ficar índexs de l'argument que han d'agafar
        for idx, key in enumerate(aux_variables):
            for n in aux_neurons:
                if n.firstlayer:
                    for i, inp in enumerate(n.inputs):
                        if isinstance(inp, Node) and inp.key == key:
                            n.inputs[i] = idx
        
        # Pas 2: agafar els inputs corresponents
        for n in aux_neurons: 
            if n.firstlayer:
                n.firstlayer = False
                for i, inp in enumerate(n.inputs):
                    if isinstance(args[inp], LogicGate):
                        n.inputs[i] = args[inp].outputn
                    elif isinstance(args[inp], Node):
                        n.inputs[i] = args[inp]
                    else:
                        raise TypeError
        
        # Pas 3: treure isoutput a les neurones out dels arguments
        for lg in args:
            if isinstance(lg, LogicGate):
                lg.outputn.isoutput = False

    # Merge que utilitza el paràmetre 'self.expression' i que
    # crida a LGCreator.create(s) on s és l'expressió de self
    # amb totes les variables canviades per les expressions 
    # dels arguments.

    def connect(self, n1, n2):
        r'''
        Adds a weigthed connection between neuron 1 and 2
        '''
        assert isinstance(n2,Neuron), 'n2 must be an instance of Neuron.'
        if isinstance(n1,Node):
            n2.inputs.append(n1)
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
