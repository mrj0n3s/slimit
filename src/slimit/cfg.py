'''
Created on 29.04.2017

@author: Mr. Jones
'''
import Queue
from slimit.visitors import constantvisitor

class FlowNode(object):
    def __init__(self):
        #nodes belonging to this FlowNode
        self.node_list = []
        #edges from this node to target nodes
        self.edge_targets = []
              
class PrintTraversal(object):
    
    def __init__(self,nodes):
        self.node_list = Queue.Queue()
        if isinstance(nodes, list):
            for i in nodes:
                self.node_list.put(i)
        else:
            self.node_list.put(nodes)
        
        
    def traverse(self):
        while(not self.node_list.empty()):
            next_node = self.node_list.get()
            print('NEW FLOW_NODE')
            for i in next_node.edge_targets:
                self.node_list.put(i)
            for i in next_node.node_list:
                print '    '+type(i).__name__
                try:
                    print '        '+i.value
                except:
                    pass
                
class ConstantTraversal(object):
    
    def __init__(self,nodes):
        self.node_list = Queue.Queue()
        self.constantVisitor = constantvisitor.ConstantVisitor()
        if isinstance(nodes, list):
            for i in nodes:
                self.node_list.put(i)
        else:
            self.node_list.put(nodes)
        
        
    def traverse(self):
        while(not self.node_list.empty()):
            next_node = self.node_list.get()
            for i in next_node.edge_targets:
                self.node_list.put(i)
            self.constantVisitor.do(next_node.node_list)
