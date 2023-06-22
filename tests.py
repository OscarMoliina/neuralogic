from neuralogic import *

print(f'\nINPUTS = {input}\n')

AND = AND()
OR = OR()
NAND = NAND()
NOR = NOR()
XOR = XOR()
XNOR = XNOR()
for i in ['AND', 'OR', 'NAND', 'NOR', 'XOR', 'XNOR']:
    prediction = eval(i).predict()
    print(f'{i}: {prediction}')
print()