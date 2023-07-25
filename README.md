# neuralogic 🧠

![alt text](https://www.cloudsavvyit.com/p/uploads/2021/05/22e2d43d.png?width=1198&trim=1,1&bg-color=000&pad=1,1)

Neuralogic is a graph based binary circuit framework whose logical units are neurons based on the first McCulloch-Pitts model of the Perceptron. This project is aimed to be useful and motivational for students who start to explore the Logical and Neural Networks fields.

---
## Usage Example
```python
from neuralogic import *

s = 'A and not B or C'
creator = LGCreator()
lg = creator.create(s=s)
pred = lg.predict()
print(f'Boolean Formula: {s}')
print('Truth table:')
print(pred)
```
Output: 
```python
>>>
Boolean Formula: A and not B or C
Truth table:
[1, 0, 1, 1, 1, 0, 1, 0]
```

---

### Done
- LogicGates Merge
- XOR example (and others!)
- New input assignment
  - Using itertools.product
  - variables initialization
- Save weigths for then merge with fixed weigths
- Documentation in DocStrings
- Hashable Nodes
- Parser
- OutputNeuron erased
- ``connect()`` as Neuron method
- created ``copy()`` as Node method
- LogicGate ``merge()`` changed working correctly 
- LogicGate.variables OrderedDict

### To-Do
- Function startInputs that takes all inputs and, in order, it assigns the correct self.out to each of them

