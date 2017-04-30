'''
Created on 29.04.2017

@author: Mr. Jones
'''

from slimit.cfg import FlowNode

class CFGVisitor():
    def visit(self,node, flow_node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node, flow_node)

    def generic_visit(self, node, flow_node):
        if node is None:
            return None
        flow_node.node_list.append(node)
        for child in node:
            self.visit(child, flow_node)
        return None
    
    def visit_Program(self, node, flow_node):
        flow_node.node_list.append(node)
        next_node = FlowNode()
        flow_node.edge_targets.append(next_node)
        for child in node.children():
            x = self.visit(child,next_node)
            if x is not None:
                next_node = x
                flow_node.edge_targets.append(x)
        return None
                       
    def visit_If(self, node, flow_node):
        flow_node.node_list.append(node)
        self.visit(node.predicate, flow_node)
        next_node1 = FlowNode()
        flow_node.edge_targets.append(next_node1)
        self.visit(node.consequent, next_node1)
        next_node2 = FlowNode()
        flow_node.edge_targets.append(next_node2)
        self.visit(node.alternative, next_node2)
        next_node = FlowNode()
        next_node1.edge_targets.append(next_node)
        next_node2.edge_targets.append(next_node)
        return next_node