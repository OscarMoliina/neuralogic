from neuralogic import *

s = 'not A and (A or B) and (A or B)'
creator = LGCreator()
lg = creator.create(s=s)
print(lg); print(creator.rpn.out)
pred = lg.predict()
print(f'Boolean Formula: {s}')
print('Truth table:')
print(pred)