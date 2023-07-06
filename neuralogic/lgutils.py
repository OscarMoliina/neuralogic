from neuralogic.nn.neuron import *

def nNOT(isout:bool = False) -> Neuron: return Neuron(tau=0, weights=[-1], isoutput=isout)
def nBuffer(isout:bool = False) -> Neuron: return Neuron(tau=1, weights=[1], isoutput=isout)

def nAND(isout:bool = False) -> Neuron: return Neuron(tau=2, weights=[1,1], isoutput=isout)
def nOR(isout:bool = False) -> Neuron: return Neuron(tau=1, weights=[1,1], isoutput=isout)

def nNAND(isout:bool = False) -> Neuron: return Neuron(tau=-1, weights=[-1,-1], isoutput=isout)
def nNOR(isout:bool = False) -> Neuron: return Neuron(tau=0, weights=[-1,-1], isoutput=isout)
