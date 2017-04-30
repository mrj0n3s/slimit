'''
Created on 30.04.2017

@author: Mr. Jones
'''
from slimit.visitors.ecmavisitor import ECMAVisitor
from slimit import ast

def visit_Program(self,node):
    if self.inject_fileoutput:
        return 'var fso = new ActiveXObject("Scripting.FileSystemObject");\nvar '+self.output_handlename+' = fso.CreateTextFile("'+self.output_handlename+'", 2, true);\n'+'\n'.join(self.visit(child) for child in node)+'\n'+self.output_handlename+'.close();'
    else:
        return '\n'.join(self.visit(child) for child in node)
def visit_Return(self,node):
    if node.expr is None:
        return 'return;'
    else:
        val = self.visit(node.expr)
        if type(node.expr).__name__ == 'Identifier' and self.inject_fileoutput:
            return self.output_handlename+'.write(%s);' % val +'return %s;' % val
        else:
            return 'return %s;' % val
        
def testFunc3(self,node,writeOutput):
    replacements = []
    for arg in node.args:
        if type(arg).__name__ == 'Identifier':
            replacements.append(arg.value)
    s = '%s(%s)' % (self.visit(node.identifier),
                    ', '.join(self.visit(arg) for arg in node.args))
    if getattr(node, '_parens', False):
        s = '(' + s + ')'
    if self.inject_fileoutput:
        self.write_injection[s]=replacements
    return s
    
def visit(self,node):
    method = 'visit_%s' % node.__class__.__name__
    if method == 'visit_FunctionCall':
        writeOutput = True
        for arg in node.args:
            if type(arg).__name__ == 'String' or type(arg).__name__ == 'Identifier': 
                writeOutput &= True
            else:
                writeOutput = False
        return self.visit_FunctionCall(node,writeOutput)
    return getattr(self, method, self.generic_visit)(node)

def ast_Node_to_ecma(self,inject = False):
    # Can't import at module level as ecmavisitor depends
    # on ast module...
    from slimit.visitors.ecmavisitor import ECMAVisitor
    visitor = ECMAVisitor()
    visitor.inject_fileoutput = inject
    if not inject:
        return visitor.visit(self)
    else:
        ret = visitor.visit(self)
        ret2 = []
        for i in ret.split('\n'):
            for j,v in visitor.write_injection.items():
                if j in i:
                    for x in v:
                        ret2.append(self.output_handlename+'.write('+x+'+\'\\n\');\n')
                    #visitor.write_injection.pop(j)
                    break
            ret2.append(i)
        return ''.join(ret2)
        
class SlimitModifications():
    
    def __init__(self,name='file123'):
        self.updateFileHandleName(name)
        
    def updateFileHandleName(self,name):
        ECMAVisitor.output_handlename = name
        ast.Node.output_handlename = name
    
    ECMAVisitor.visit_Program = visit_Program
    ECMAVisitor.visit_Return = visit_Return
    ECMAVisitor.visit = visit
    ECMAVisitor.visit_FunctionCall = testFunc3
    ECMAVisitor.write_injection = dict()
    ECMAVisitor.inject_fileoutput = False
    ast.Node.to_ecma = ast_Node_to_ecma