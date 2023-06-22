from neuralogic import *

print(input)
print(input1D)

AND = AND()
OR = OR()
NAND = NAND()
NOR = NOR()
ManualXOR = ManualXOR()
NOT = NOT()
for i in [AND, OR, NAND, NOR, ManualXOR, NOT]:
    prediction = i.predict()
    print(prediction)