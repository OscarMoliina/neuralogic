from neuralogic.logicgate import LogicGate
from neuralogic.nn.neuron import Neuron, OutputNeuron, Node

def Buffer() -> LogicGate:
    lg = LogicGate(variables=1)
    n = OutputNeuron(tau=1, firstlayer=True)
    lg.add(n)
    lg.connect(lg.inputs[0], n, 1)
    return lg

def NOT() -> LogicGate:
    lg = LogicGate(variables=1)
    n = OutputNeuron(tau=0, firstlayer=True)
    lg.add(n)
    lg.connect(lg.inputs[0], n, -1)
    return lg

def AND() -> LogicGate:
    lg = LogicGate(variables=2)
    n = OutputNeuron(tau=2, firstlayer=True)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, 1)
    return lg

def OR() -> LogicGate:
    lg = LogicGate(variables=2)
    n = OutputNeuron(tau=1, firstlayer=True)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, 1)
    return lg

def ManualNAND() -> LogicGate:
    lg = LogicGate(variables=2)
    n = OutputNeuron(tau=-1, firstlayer=True)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, -1)
    return lg

def ManualNOR() -> LogicGate:
    lg = LogicGate(variables=2)
    n = OutputNeuron(tau=0, firstlayer=True)
    lg.add(n)
    for i in lg.inputs:
        lg.connect(i, n, -1)
    return lg

def ManualXOR() -> LogicGate:
    lg = LogicGate(variables=2)
    AND = OutputNeuron(tau=2)
    OR = Neuron(tau=1, firstlayer=True)
    NAND = Neuron(tau=-1, firstlayer=True)
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

def NAND() -> LogicGate:
    FINAL = NOT()
    AND_ = AND()
    FINAL.merge(AND_)
    return FINAL

def NOR() -> LogicGate:
    FINAL = NOT()
    OR_ = OR()
    FINAL.merge(OR_)
    return FINAL

def XOR() -> LogicGate:
    FINAL = AND()
    OR_ = OR()
    NAND_ = NAND()
    FINAL.merge(OR_, NAND_)
    return FINAL

def XNOR() -> LogicGate:
    FINAL = NOT()
    XOR_ = XOR()
    FINAL.merge(XOR_)
    return FINAL