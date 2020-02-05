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
        # Implement me!
        pass
    def NNF(self):
        # Implement me!
        pass
    def getVars(self):
        # Implement me!
        pass
    def simplify(self):
        # Implement me!
        pass
    def indented(self,d):
        return TABWIDTH*d*' ' + "Not\n" + self.exp.indented(d + 1) + "\n"
    def removeImplications(self):
        # Implement me!
        pass
    def isLiteral(self):
        # Implement me!
        pass
    def isNNF(self):
        # Implement me!
        pass


class And(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " & " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\land " + self.exp2.tex() + ")"
    def eval(self, interp):
        # Implement me!
        pass
    def NNF(self):
        # Implement me!
        pass
    def getVars(self):
        # Implement me!
        pass
    def simplify(self):
        # Implement me!
        pass
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "And\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        # Implement me!
        pass
    def isLiteral(self):
        # Implement me!
        pass
    def isNNF(self):
        # Implement me!
        pass


class Or(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " | " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\lor " + self.exp2.tex() + ")"
    def eval(self, interp):
        # Implement me!
        pass
    def NNF(self):
        # Implement me!
        pass
    def getVars(self):
        # Implement me!
        pass
    def simplify(self):
        # Implement me!
        pass
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Or\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        # Implement me!
        pass
    def isLiteral(self):
        # Implement me!
        pass
    def isNNF(self):
        # Implement me!
        pass

class Implies(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " => " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Rightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        # Implement me!
        pass
    def NNF(self):
        # Implement me!
        pass
    def getVars(self):
        # Implement me!
        pass
    def simplify(self):
        # Implement me!
        pass
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Implies\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1) + "\n"
        return result
    def removeImplications(self):
        # Implement me!
        pass
    def isLiteral(self):
        # Implement me!
        pass
    def isNNF(self):
        # Implement me!
        pass

class Iff(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " <=> " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Leftrightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        val1 = self.exp1.eval(interp)
        val2 = self.exp2.eval(interp)
        return BoolConst(val1.val == val2.val)
    def NNF(self):
        return Iff(self.exp1.NNF(), self.exp2.NNF())
    def getVars(self):
        # Implement me!
        pass
    def simplify(self):
        # Implement me!
        pass
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Iff\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        # Implement me!
        pass
    def isLiteral(self):
        # Implement me!
        pass
    def isNNF(self):
        # Implement me!
        pass

    

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
