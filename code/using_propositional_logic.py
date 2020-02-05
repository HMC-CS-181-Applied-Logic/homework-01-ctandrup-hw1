from propositional_logic import *


T = BoolConst(True)
F = BoolConst(False)

A = BoolVar('A')
B = BoolVar('B')
C = BoolVar('C')

f1 = And(A,B)
f2 = Or(Not(B),C)
f3 = Iff(f1,f2)

print('')
print("Formula 33, object constructor representation:")
print(f3)

print('')
print("Formula f3, formatted ASCII:")
print(f3.format())

print('')
print("Formula f3, LaTeX:")
print(f3.tex())

print('')
print("Formula f3, Indented tree representation:")
f3.treeView()
