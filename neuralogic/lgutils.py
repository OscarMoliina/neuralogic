from neuralogic.nn.neuron import *

#UnitaryNeurons
def NOTNeuron() -> Neuron: return Neuron(tau=0, weights=[-1])
def BufferNeuron() -> Neuron: return Neuron(tau=1, weights=[1])

#BinaryNeurons
def ANDNeuron() -> Neuron: return Neuron(tau=2, weights=[1,1])
def ORNeuron() -> Neuron: return Neuron(tau=1, weights=[1,1])
def NANDNeuron() -> Neuron: return Neuron(tau=-1, weights=[-1,-1])
def NORNeuron() -> Neuron: return Neuron(tau=0, weights=[-1,-1])
