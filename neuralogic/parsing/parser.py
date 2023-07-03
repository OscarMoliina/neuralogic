from neuralogic.logicgate import LogicGate
from neuralogic.gates import *
from typing import Any, List, Tuple, Literal

ops = {
    'not' : (NOT(), 1, 1),
    'and' : (AND(), 0, 2),
    'or'  : (OR(),  0, 2),
    'xor' : (XOR(), 0, 2),
    'nand': (NAND(),0, 2),
    'nor' : (NOR(), 0, 2),
    'xnor': (XNOR(),0, 2)
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
        self.lg = LogicGate(variables=len(self.rpn.operands))
        operandsdic = {op:self.lg.inputs[idx] for idx,op in enumerate(self.rpn.operands)}
        
        while f:
            el = f[0]
            if el in self.rpn.operands:
                self.varstack.append(operandsdic[el])
                f.remove(el)
            elif el in self.rpn.OPS:
                # Create a Logic Gate
                lg = ops[el][0]
                if ops[el][2] == 1:
                    lg.merge(self.varstack.pop())
                elif ops[el][2] == 2:
                    lg.merge(self.varstack.pop(), self.varstack.pop())
                self.varstack.append(lg)
                f.remove(el)

        self.lg = self.varstack[0]

        return self.lg

