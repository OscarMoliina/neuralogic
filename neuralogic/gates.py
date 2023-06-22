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
    for i in range(len(lg.inputs)):
        lg.connect(lg.inputs[i], n, 1)
    return lg

def NAND() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=-1)
    lg.add(n)
    for i in range(len(lg.inputs)):
        lg.connect(lg.inputs[i], n, -1)
    return lg

def OR() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=1)
    lg.add(n)
    for i in range(len(lg.inputs)):
        lg.connect(lg.inputs[i], n, 1)
    return lg

def NOR() -> LogicGate:
    lg = LogicGate(inputs=input)
    n = OutputNeuron(tau=0)
    lg.add(n)
    for i in range(len(lg.inputs)):
        lg.connect(lg.inputs[i], n, -1)
    return lg

def XOR() -> LogicGate:
    lg = LogicGate(inputs=input)
    lg.add(AND())
    lg.add(OR())
    lg.add(NAND())
    lg.connect(NAND,AND,-1)
    lg.connect(OR,AND,1)
    return lg
