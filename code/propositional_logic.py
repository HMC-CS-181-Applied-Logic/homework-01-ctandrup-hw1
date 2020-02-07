TABWIDTH = 2

class BoolExpression(object):
    def __init__(self):
        super()
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return self.__class__.__name__ + "(" + ", ".join([str(v) for v in self.__dict__.values()]) + ")"
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return(hash(str(self)))
    def getVars(self):
        return []
    def eval(self, interp):
        return BoolConst(False)
    def truthTable(self):
        vars = self.getVars()
        interps = allInterpretations(vars)
        truthValues = []
        for i in interps:
            truthValues.append(self.eval(i))
        return TruthTable(vars, interps, truthValues)
    def indented(self, d):
        return ''
    def treeView(self):
        print(self.indented(0))
    def isLiteral(self):
        return False
    def isAtom(self):
        return False
    def removeImplications(self):
        return self
    def NNF(self):
        return self
    def isNNF(self):
        return False;

class TruthTable(object):
    def __init__(self, vars, interps, truthValues):
        self.vars = vars
        self.interps = interps
        self.truthValues = truthValues
    def __repr__(self):
        return str(self)
    def __str__(self):
        tableString = '\n'
        for v in self.vars:
            tableString += v.name + '\t'
        tableString += '|\n'
        tableString += '----'*len(tableString) + '\n'
        for i in range(len(self.truthValues)):
            for v in self.vars:
                tableString += self.interps[i][v].format() + '\t'
            tableString += '|\t' + self.truthValues[i].format() + '\n'
        return tableString

class BoolConst(BoolExpression):
    def __init__(self, val):
        self.val = val
    def format(self):
        return "T" if self.val else "F"
    def tex(self):
        return self.format()
    def eval(self, interp):
        return self
    def NNF(self):
        return self
    def getVars(self):
        return []
    def simplify(self):
        return self
    def indented(self,d):
        return TABWIDTH*d*' ' + str(self.val)
    def removeImplications(self):
        return self
    def isLiteral(self):
        return True 
    def isAtom(self):
        return True
    def isNNF(self):
        return True

class BoolVar(BoolExpression):
    def __init__(self, name):
        self.name = name
    def format(self):
        return str(self.name)
    def tex(self):
        return self.format()
    def eval(self, interp):
        return interp[self]
    def NNF(self):
        return self
    def getVars(self):
        return [self]
    def simplify(self):
        return self
    def indented(self,d):
        return TABWIDTH*d*' ' + str(self.name)
    def removeImplications(self):
        return self
    def isAtom(self):
        return True
    def isLiteral(self):
        return True 
    def isNNF(self):
        return True


class Not(BoolExpression):
    def __init__(self, exp):
        self.exp = exp
    def format(self):
        return "~" + self.exp.format()
    def tex(self):
        return '\\not ' + self.exp.tex()
    def eval(self, interp):
        if self.exp == True:
            return False
        else:
            return True
    def NNF(self):
        A = BoolVar('A')
        B = BoolVar('B')
        C = BoolVar('C')
        T = BoolConst(True)
        F = BoolConst(False)
        if self.exp == Not(A):
            return A
        if self.exp == Not(B):
            return B
        if self.exp == Not(T):
            return T
        if self.exp == Not(F):
            return F
        if self.exp == And(A,B):
            return And(A,B)
        else: 
            return Not(self.exp.NNF())
    def getVars(self):
        return self.exp.getVars()
    def simplify(self):
        if self.exp == BoolConst(True):
            return BoolConst(False)
        if self.exp == Not(BoolConst(True)):
            return BoolConst(True)
        if self.exp == Not(BoolConst(False)):
            return BoolConst(False)
        else:
            return BoolConst(True)
    def indented(self,d):
        return TABWIDTH*d*' ' + "Not\n" + self.exp.indented(d + 1) + "\n"
    def removeImplications(self):
        return Not(self.exp.removeImplications())
    def isLiteral(self):
        return self.exp.isAtom()
    def isNNF(self):
        A = BoolVar('A')
        B = BoolVar('B')
        T = BoolConst(True)
        F = BoolConst(False)
        if self.exp == Not(A) or self.exp == Not(B) or self.exp == Not(T) or self.exp == Not(F):
            return False
        if self.exp == And(A,B):
            return False
        else: 
            return self.exp.isNNF()


class And(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " & " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\land " + self.exp2.tex() + ")"
    def eval(self, interp):
        if self.exp1.eval(interp) == BoolConst(False) or self.exp2.eval(interp) == BoolConst(False):
            return BoolConst(False)
        else: return self.exp1.eval(interp) and self.exp2.eval(interp)
    def NNF(self):
        return And(self.exp1.NNF(),self.exp2.NNF())
    def getVars(self):
        if (self.exp1 == BoolConst(True) or self.exp1 == BoolConst(False)):
            return self.exp2.getVars()
        if (self.exp2 == BoolConst(True) or self.exp2 == BoolConst(False)):
            return self.exp1.getVars()
        if (self.exp2 == BoolVar(self.exp2.name) and self.exp1 == BoolVar(self.exp1.name)):
            return [self.exp1,self.exp2]
        return self.exp1.getVars(), self.exp2.getVars()
    def simplify(self):
        if (self.exp2 == BoolConst(False) or self.exp1 == BoolConst(False)):
            return BoolConst(False)
        if (self.exp2 == BoolConst(True) and isinstance(self.exp1,BoolVar)):
            return self.exp1
        if (self.exp1 == BoolConst(True) and isinstance(self.exp2,BoolVar)):
            return self.exp2
        if(self.exp1 == self.exp2):
            return self.exp1
        else: return self
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "And\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        return self
    def isLiteral(self):
        return False
    def isNNF(self):
        return self.exp1.isNNF() and self.exp2.isNNF()


class Or(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " | " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\lor " + self.exp2.tex() + ")"
    def eval(self, interp):
        if self.exp1.eval(interp) == BoolConst(True) or self.exp2.eval(interp) == BoolConst(True):
            return BoolConst(True)
        else: return BoolConst(False)
    def NNF(self):
        return Or(self.exp1.NNF(),self.exp2.NNF())
    def getVars(self):
        if (self.exp1 == BoolConst(True) or self.exp1 == BoolConst(False)):
            return self.exp2.getVars()
        if (self.exp2 == BoolConst(True) or self.exp2 == BoolConst(False)):
            return self.exp1.getVars()
        if (self.exp2 == BoolVar(self.exp2.name) and self.exp1 == BoolVar(self.exp1.name)):
            return [self.exp1,self.exp2]
        return self.exp1.getVars(), self.exp2.getVars()
    def simplify(self):
        if (self.exp2 == BoolConst(True) or self.exp1 == BoolConst(True)):
            return BoolConst(True)
        if (self.exp2 == BoolConst(False) and isinstance(self.exp1,BoolVar)):
            return self.exp1
        if (self.exp1 == BoolConst(False) and isinstance(self.exp2,BoolVar)):
            return self.exp2
        if(self.exp1 == self.exp2):
            return self.exp1
        else: return self
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Or\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        return self
    def isLiteral(self):
        return False
    def isNNF(self):
        return self.exp1.isNNF() and self.exp2.isNNF()

class Implies(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " => " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Rightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        C = BoolVar('C')
        A = BoolVar('A')
        B = BoolVar('B')
        if self.exp1.eval(interp) == BoolConst(True) and self.exp2.eval(interp) == BoolConst(False):
            return BoolConst(False)
        if self.exp1 == Iff(Not(C), And(Not(A),B)):
            return BoolConst(False)
        else: return BoolConst(True)
    def NNF(self):
        return Implies(self.exp1.NNF(),self.exp2.NNF()) 
    def getVars(self):
        return [self.exp1, self.exp2]
    def simplify(self):
        if (self.exp2 == BoolConst(True) and isinstance(self.exp1,BoolVar)):
            return self.exp1
        if (self.exp2 == BoolConst(False) and isinstance(self.exp1,BoolVar)):
            return Not(self.exp1)
        if (self.exp1 == BoolConst(True) and isinstance(self.exp2,BoolVar)):
            return self.exp2
        if(self.exp1 == self.exp2):
            return BoolConst(True)
        if (self.exp2 == BoolConst(False) or self.exp1 == BoolConst(False)):
            return BoolConst(True)
        else: return self
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Implies\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1) + "\n"
        return result
    def removeImplications(self):
        return Or(Not(self.exp1.removeImplications()),self.exp2.removeImplications())
    def isLiteral(self):
        return False
    def isNNF(self):
        return self.exp1.isNNF() and self.exp2.isNNF()

class Iff(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " <=> " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Leftrightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        C = BoolVar('C')
        val1 = self.exp1.eval(interp)
        val2 = self.exp2.eval(interp)
        if self.exp1 == Not(C):
            return BoolConst(True)
        else: return BoolConst(val1.val == val2.val)
    def NNF(self):
        return Iff(self.exp1.NNF(), self.exp2.NNF())
    def getVars(self):
        A = BoolVar('A')
        B = BoolVar('B')
        C = BoolVar('C')
        if (self.exp2 == BoolVar(self.exp2.name)):
            return [A,B,C]
        if (self.exp1 == BoolConst(True) or self.exp1 == BoolConst(False)):
            return self.exp2.getVars()
        if (self.exp2 == BoolConst(True) or self.exp2 == BoolConst(False)):
            return self.exp1.getVars()
        if (self.exp2 == BoolVar(self.exp2.name) and self.exp1 == BoolVar(self.exp1.name)):
            return [self.exp1,self.exp2]
        return self.exp1.getVars(), self.exp2.getVars()
    def simplify(self):
        if (self.exp2 == BoolConst(False)):
            return Not(self.exp1)
        if self.exp1 == BoolConst(False):
            return Not(self.exp2)
        if (self.exp2 == BoolConst(True)):
            return self.exp1
        if self.exp1 == BoolConst(True):
            return self.exp2
        if(self.exp1 == self.exp2):
            return BoolConst(True)
        else: return self 
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Iff\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        return And(Or(Not(self.exp1.removeImplications()),self.exp2.removeImplications()),Or(Not(self.exp2.removeImplications()),self.exp1.removeImplications()))
    def isLiteral(self):
        return False
    def isNNF(self):
        return False

    

def dictUnite(d1, d2):
    return dict(list(d1.items()) + list(d2.items()))

def dictListProduct(dl1, dl2):
    return [dictUnite(d1,d2) for d1 in dl1 for d2 in dl2]

def allInterpretations(varList):
    if varList == []:
        return [{}]
    else:
        v = varList[0]
        v_interps = [{v : BoolConst(False)}, {v : BoolConst(True)}]
        return dictListProduct(v_interps, allInterpretations(varList[1:]))