from neuralogic import *

print(input)
for i in [AND(), OR(), NAND(), NOR(), XOR()]:
    prediction = i.predict()
    print(prediction)