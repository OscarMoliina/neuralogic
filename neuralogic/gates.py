from neuralogic.logicgate import LogicGate
from neuralogic.nn.neuron import Neuron, OutputNeuron, Node
from neuralogic.lgutils import *

def buildLG(neuron) -> LogicGate:
    n = neuron()
    lg = LogicGate(numvars=len(n.weights))
    n.isoutput = True
    n.firstlayer = True
    lg.add(n)
    for i in range(lg.numvars):
        lg.connect(lg.inputs[i], n, n.weights[i])
    return lg

def Buffer() -> LogicGate: return buildLG(neuron=BufferNeuron) 
def NOT() -> LogicGate: return buildLG(neuron=NOTNeuron)
def AND() -> LogicGate: return buildLG(neuron=ANDNeuron)
def OR() -> LogicGate: return buildLG(neuron=ORNeuron)
def ManualNAND() -> LogicGate: return buildLG(neuron=NANDNeuron)
def ManualNOR() -> LogicGate: return buildLG(neuron=NORNeuron)

def ManualXOR() -> LogicGate:
    lg = LogicGate(numvars=2)
    AND = ANDNeuron()
    AND.isoutput = True
    OR = ORNeuron()
    OR.firstlayer = True
    NAND = NANDNeuron()
    NAND.firstlayer = True
    lg.add(AND)
    lg.add(OR)
    lg.add(NAND)
    for i in range(lg.numvars):
        lg.connect(lg.inputs[i], OR, OR.weights[i])
    for i in range(lg.numvars):
        lg.connect(lg.inputs[i], NAND, NAND.weights[i])
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