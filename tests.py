from neuralogic import *

print(input)
print(input1D)

AND = AND()
OR = OR()
NAND = NAND()
NOR = NOR()
XOR = XOR()
NOT = NOT()
for i in [AND, OR, NAND, NOR, XOR, NOT]:
    prediction = i.predict()
    print(prediction)