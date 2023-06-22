from neuralogic.logicgate import LogicGate
from neuralogic.nn.neuron import Neuron, OutputNeuron, Node

input = [
    (0,0),
    (0,1),
    (1,0),
    (1,1)
]

def AND() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=2)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, 1)
    return lg

def NAND() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=-1)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, -1)
    return lg

def OR() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=1)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, 1)
    return lg

def NOR() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=0)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, -1)
    return lg

def ManualXOR() -> LogicGate:
    lg = LogicGate(inputs=input)
    AND = OutputNeuron(tau=2)
    OR = Neuron(tau=1)
    NAND = Neuron(tau=-1)
    lg.add(AND)
    lg.add(OR)
    lg.add(NAND)
    for i in lg.inputs:
        lg.connect(i, OR, 1)
    for i in lg.inputs:
        lg.connect(i, NAND, -1)
    lg.connect(OR, AND, 1)
    lg.connect(NAND, AND, 1)
    return lg

def XOR() -> LogicGate:
    lg = LogicGate(inputs=input)
    AND = AND()
    OR = OR()
    NAND = NAND()

