'''
Created on 29.04.2017

@author: Mr. Jones
'''
from slimit.visitors.replacementvisitor import ReplacementVisitor

def checkNodeType(node,varName):
    return type(node).__name__ == varName

class FoldingVisitor():
        
    def __init__(self):
        self.concatenated = 0
        self.replacement = ReplacementVisitor()
    
    def do(self,tree):
        self.visit(tree, tree)
        while self.concatenated == 1:
            self.concatenated = 0
            self.visit(tree,tree)
    
    def visit(self, node,parent):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node,parent)

    def generic_visit(self, node,parent):
        for child in node:
            self.visit(child,parent)
            
    #I tried to avoid using eval
    #make sure that value is always a string value
    def visit_BinOp(self,node,parent):
        if node.op == '-':
            if checkNodeType(node.left,'Number') and checkNodeType(node.right,'Number'):
                node.left.value = str(int(node.left.value)-int(node.right.value))
                self.concatenated |= self.replacement.visit(parent,node,node.left)
        elif node.op == '+':
            if checkNodeType(node.left,'Number') and checkNodeType(node.right,'Number'):
                node.left.value = str(int(node.left.value)+int(node.right.value))
                self.concatenated |= self.replacement.visit(parent,node,node.left)
            '''if checkNodeType(node.left,'String') and checkNodeType(node.right,'String'):
                node.left.value = '\''+str(node.left.value[1:len(node.left.value)-1])+str(node.right.value[1:len(node.right.value)-1])+'\''
                self.concatenated |= self.replacement.visit(parent,node,node.left)'''
            '''elif checkNodeType(node.left, 'BinOp') and checkNodeType(node.right,'String'):
                if checkNodeType(node.left.right,'String'):
                    node.left.right.value = '\''+str(node.left.right.value[1:len(node.left.right.value)-1])+str(node.right.value[1:len(node.right.value)-1])+'\''
                    self.concatenated |= self.replacement.visit(parent,node,node.left)
                    #TODO remove workaround for error:
                    #var isduwcL = pcDRW['ExpandEnvironmentStrings']('%TEMP%') + '/' + 'lynt' + 'a';
                    if not checkNodeType(node.left.left,'BinOp'):
                        node.right.value = '''''
        for child in node:
            self.visit(child,node)
    
    def visit_Comma(self,node,parent):
        if checkNodeType(node.left,'String') and checkNodeType(node.right,'String'):
            node.left.value = '\''+str(node.right.value[1:len(node.right.value)-1])+'\''
            self.concatenated |= self.replacement.visit(parent,node,node.left)
        for child in node:
            self.visit(child,node)