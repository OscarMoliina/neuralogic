from neuralogic.logicgate import LogicGate
from neuralogic.gates import *
from neuralogic.lgutils import *
from typing import Any, List, Tuple, Literal

#print(NAND())
ops = {
    #str, logicgate, preference, numvars, neuron
    'not' : (NOT, 1, 1, NOTNeuron),
    'and' : (AND, 0, 2, ANDNeuron),
    'or'  : (OR,  0, 2, ORNeuron),
    'nand': (NAND,0, 2, NANDNeuron),
    'nor' : (NOR, 0, 2, NORNeuron),
}

class RPN:
    def __init__(self) -> None:
        self.OPS = list(ops.keys())
        self.precedence = {k:op[1] for k,op in ops.items()}
    
    def __call__(self, logicformula:str) -> List[str]:
        r'''
        Executes the Shunting Yard algorithm to convert the infix
        formula's notation to a postfix or Reverse Polish Notation.
        '''
        self.operands = []
        self.out = []
        self.stack = []
        
        def tokenize(str) -> List[str]:
            l = []
            for token in str.split():
                if '(' in token[0]:
                    l.append(token[0]); l.append(token[1:])
                elif ')' in token[-1]:
                    l.append(token[:-1]); l.append(token[-1])
                else:
                    l.append(token)
            return l
        
        for t in tokenize(str=logicformula):
            if t == '(':
                self.stack.append(t)
            elif t == ')':
                while self.stack and self.stack[-1] != '(':
                    self.out.append(self.stack.pop())
                if self.stack and self.stack[-1] == '(':
                    self.stack.pop()
            elif t in self.OPS:
                while (self.stack and 
                       self.stack[-1] != '(' and
                       self.precedence[t] <= self.precedence[self.stack[-1]]):
                    self.out.append(self.stack.pop())
                self.stack.append(t)
            else:
                if t not in self.operands:
                    self.operands.append(t)
                self.out.append(t)
        
        while self.stack:
            self.out.append(self.stack.pop())

        return self.out

class LGCreator:
    def __init__(self) -> None:
        self.rpn = RPN()
        self.varstack = [] #stack for variables
        self.args = [op[2] for op in ops.values()]

    def create(self, s:str) -> LogicGate:
        r'''
        Creates a LogicGate with a boolean formula as an input.
        '''
        f = self.rpn(s) #formula
        self.lg = LogicGate(numvars=len(self.rpn.operands))
        operandsdic = {op:self.lg.inputs[idx] for idx,op in enumerate(self.rpn.operands)}
        
        #Etiquetem les variables
        for k,v in operandsdic.items():
            v.key = str(k)

        while f:
            el = f[0]
            f.remove(el)
            if el in operandsdic.keys():
                self.varstack.append(operandsdic[el])
            elif el in self.rpn.OPS:
                #Add a neuron of its type
                n = ops[el][3]()
                n.key = el.upper()
                if not f: 
                    n.isoutput = True
                self.lg.add(n)
                for idx in range(ops[el][2]):
                    node = self.varstack.pop()
                    if not isinstance(node,Neuron):
                        n.firstlayer = True
                    self.lg.connect(n1=node,
                                    n2=n)
                self.varstack.append(n)

        return self.lg

