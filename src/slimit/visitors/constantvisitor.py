'''
Created on 29.04.2017

@author: Mr. Jones
'''

class ConstantVisitor():
    
    '''used on flow graph basic blocks'''
    def __init__(self):
        #for each variable save the 
        self.var_declarations = dict()
        
    def visit(self,node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        if node is None:
            return None
    
    def do(self,list_nodes):
        for node in list_nodes:
            self.visit(node)
    
    def visit_VarDecl(self, node):
        #print(node.initializer)
        if node.initializer is not None:
            self.var_declarations[node.identifier.value] = node.initializer.value
        print(self.var_declarations)
            
    def visit_Assign(self,node):
        if node.op == '=':
            if hasattr(node.left, 'value'):
                if node.left.value in self.var_declarations:
                    if hasattr(node.right, 'value'):
                        self.var_declarations[node.left.value] = node.right.value
    
    def visit_BinOp(self,node):
        for child in node.children():
            print(child)
            if hasattr(child, 'value'):
                if child.value in self.var_declarations:
                    child.value = self.var_declarations[child.value]
                
