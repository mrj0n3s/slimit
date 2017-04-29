'''
Created on 22.04.2017

@author: Mr. Jones
'''
class ReplacementVisitor():
    def visit(self,node,target,replacement):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node,target,replacement)

    def generic_visit(self, node,target,replacement):
        if node is None:
            return
        ret = 0
        if isinstance(node, list):
            for child in node:
                ret |= self.visit(child,target,replacement)
        else:
            print('unsupported replacement',node)
        return ret
    
    def visit_If(self,node,target,replacement):
        if node.predicate == target:
            node.predicate = replacement
            return 1
        elif node.consequent == target:
            node.consequent = replacement
            return 1
        elif node.alternative == target:
            node.alternative = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Try(self,node,target,replacement):
        if target in node.statements:
            node.statements.remove(target)
            node.statements.append(replacement)
            return 1
        if node.catch == target:
            node.catch = replacement
            return 1
        if node.fin == target:
            node.fin = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Catch(self,node,target,replacement):
        if target in node.elements:
            node.elements.remove(target)
            node.elements.append(replacement)
            return 1
        if node.identifier == target:
            node.identifier = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_UnaryOp(self,node,target,replacement):
        if node.op == target:
            node.op = replacement
            return 1
        if node.value == target:
            node.value = replacement
            return 1
        if node.postfix == target:
            node.postfix = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Assign(self,node,target,replacement):
        if node.left == target:
            node.left = replacement
            return 1
        elif node.right == target:
            node.right = replacement
            return 1
        elif node.op == target:
            node.op = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_FuncBase(self,node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1
        elif target in node.parameters:
            node.parameters.remove(target)
            node.parameters.append(replacement)
            return 1
        elif target in node.elements:
            node.elements.remove(target)
            node.elements.append(replacement)
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_FuncDecl(self,node,target,replacement):
        return self.visit_FuncBase(node, target, replacement)
    
    def visit_FuncExpr(self,node,target,replacement):
        return self.visit_FuncBase(node, target, replacement)
    
    def visit_BracketAccessor(self,node,target,replacement):
        if node.node == target:
            node.node = replacement
            return 1
        elif node.expr == target:
            node.expr = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_no_children(self, node,target,replacement):
        if node.value == target:
            node.value = replacement
            return 1
        return 0
    
    def visit_Identifier(self, node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_String(self, node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_Number(self, node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_EmptyStatement(self, node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_Debugger(self,node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_Regex(self,node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_Null(self,node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_Boolean(self,node,target,replacement):
        return self.visit_no_children(node,target,replacement)
    
    def visit_FunctionCall(self, node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1
        if target in node.args:
            node.args.remove(target)
            node.args.append(replacement)
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_DotAccessor(self,node,target,replacement):
        if node.node == target:
            node.node = replacement
            return 1
        if node.identifier == target:
            node.identifier = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Conditional(self,node,target,replacement):
        if node.predicate == target:
            node.predicate = replacement
            return 1
        if node.consequent == target:
            node.consequent = replacement
            return 1
        if node.alternative == target:
            node.alternative = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_While(self,node,target,replacement):
        if node.predicate == target:
            node.predicate = replacement
            return 1
        if node.statement == target:
            node.statement = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_DoWhile(self,node,target,replacement):
        return self.visit_While(node, target, replacement)
    
    def visit_Return(self,node,target,replacement):
        if node.expr == target:
            node.expr = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Break(self,node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Continue(self,node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_For(self,node,target,replacement):
        if node.init == target:
            node.init = replacement
            return 1
        if node.cond == target:
            node.cond = replacement
            return 1
        if node.count == target:
            node.count = replacement
            return 1
        if node.statement == target:
            node.statement = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_ForIn(self,node,target,replacement):
        if node.item == target:
            node.item = replacement
            return 1
        if node.iterable == target:
            node.iterable = replacement
            return 1
        if node.statement == target:
            node.statement = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Object(self,node,target,replacement):
        ret = 0
        if target in node.properties:
            node.properties.remove(target)
            node.properties.append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_NewExpr(self, node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1
        if target in node.args:
            node.args.remove(target)
            node.args.append(replacement)
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Array(self,node,target,replacement):
        ret = 0
        if target in node.items:
            node.items.remove(target)
            node.items.append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_VarStatement(self,node,target,replacement):
        ret = 0
        if target in node._children_list:
            node._children_list.remove(target)
            node._children_list.append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_Program(self,node,target,replacement):
        ret = 0
        if target in node._children_list:
            node._children_list.remove(target)
            node._children_list.append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_Block(self,node,target,replacement):
        ret = 0
        if target in node._children_list:
            node._children_list.remove(target)
            node._children_list.append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_This(self,node,target,replacement):
        ret = 0
        if target in node.children():
            node.children().remove(target)
            node.children().append(replacement)
            return 1
        for child in node:
            ret |= self.visit(child,target,replacement)
        return ret
    
    def visit_ExprStatement(self,node,target,replacement):
        if node.expr == target:
            node.expr = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_Comma(self,node,target,replacement):
        if node.left == target:
            node.left = replacement
            return 1
        elif node.right == target:
            node.right = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
    
    def visit_VarDecl(self,node,target,replacement):
        if node.identifier == target:
            node.identifier = replacement
            return 1 
        elif node.initializer == target:
            node.initializer = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret
            
            
    def visit_BinOp(self,node,target,replacement):
        if node.left == target:
            node.left = replacement
            return 1
        elif node.right == target:
            node.right = replacement
            return 1
        ret = 0
        for child in node:
            ret |= self.visit(child, target, replacement)
        return ret