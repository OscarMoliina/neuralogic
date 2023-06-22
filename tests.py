from neuralogic import *

print(input)
AND = AND()
OR = OR()
NAND = NAND()
NOR = NOR()
ManualXOR = ManualXOR()
for i in [AND, OR, NAND, NOR, ManualXOR]:
    prediction = i.predict()
    print(prediction)