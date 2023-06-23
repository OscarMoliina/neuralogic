from neuralogic import *

AND = AND()
OR = OR()
NAND = NAND()
NOR = NOR()
XOR = XOR()
XNOR = XNOR()
print()
for i in ['AND', 'OR', 'NAND', 'NOR', 'XOR', 'XNOR']:
    prediction = eval(i).predict()
    print(f'{i}: {prediction}')
print()