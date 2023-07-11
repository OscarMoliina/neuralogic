from neuralogic.nn.neuron import *

#UnitaryNeurons
def NOTNeuron() -> Neuron: return Neuron(tau=0, weights=[-1], key='NOT')
def BufferNeuron() -> Neuron: return Neuron(tau=1, weights=[1], key='Buf')

#BinaryNeurons
def ANDNeuron() -> Neuron: return Neuron(tau=2, weights=[1,1], key='AND')
def ORNeuron() -> Neuron: return Neuron(tau=1, weights=[1,1], key='OR')
def NANDNeuron() -> Neuron: return Neuron(tau=-1, weights=[-1,-1], key='NAND')
def NORNeuron() -> Neuron: return Neuron(tau=0, weights=[-1,-1], key='NOR')
