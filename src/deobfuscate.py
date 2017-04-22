#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 18.04.2017

@author: Mr. Jones
'''
#pip.exe install https://pypi.python.org/packages/ce/3d/1f9ca69192025046f02a02ffc61bfbac2731aab06325a218370fd93e18df/ply-3.10.tar.gz
#pip install jsbeautifier
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
from slimit import minify
from slimit.visitors.concatvisitor import ConcatVisitor
from slimit.visitors.nodevisitor import ASTVisitor
from slimit.scope import SymbolTable
from slimit.visitors.scopevisitor import (
    ScopeTreeVisitor,
    fill_scope_references,
    mangle_scope_tree,
    UnusedVariablesVisitor,
    )
from slimit.visitors.minvisitor import ECMAMinifier
import jsbeautifier
from jsbeautifier import Tokenizer,Output
import re
from pip._vendor.html5lib.constants import replacementCharacters

def cleanLeadingZeros(text):
    return re.sub(r"(?<!\d)0+(?=\d+)", "",text)

class varObject():
    def __init__(self,varName,value,isDefined = 0):
        self.varName = varName
        self.value = value
        self.usageCount = 0
        self.isDefined = isDefined

class TestVisitor(ASTVisitor):
    
    def __init__(self):
        self.scopeChain = []
        
    def createNewScope(self,node):
        return type(node).__name__ == 'Program' or type(node).__name__ == 'FuncDecl' or type(node).__name__ == 'FuncExpr'
    
    
    def isVarDefined(self,varname):
        for i in self.scopeChain:
            for j in i:
                if j.isDefined:
                    return True
        return False
    
    def printScope(self,scope,node):
        if type(node).__name__ == 'Program':
            print 'Variables declared in global Scope'
            for key,value in scope.items():
                print('Variable',value.varName,value.value,value.usageCount)
        else:
            print 'Variables declared in function',node.identifier.value
            for key,value in scope.items():
                print('Variable',value.varName,value.value)
            
    def checkForLeaks(self):
        for key,value in self.scopeChain[-1].items():
            if self.scopeChain[-1].get(key).isDefined == 0:
                print('Leaked Variable',key)
            
    
    def generic_visit(self, node):
        """Visit object literal."""
        print(node)
        if (self.createNewScope(node)):
            self.scopeChain.append(dict())
        for child in node:
            self.visit(child)
        if (self.createNewScope(node)):
            #print(assignments,'assignments')
            self.checkForLeaks()
            self.printScope(self.scopeChain.pop(),node)
            
    def visit_Assign(self, node):
        if node.left.value not in self.scopeChain[-1]:
            pass
            #self.scopeChain[-1][node.left.value] = varObject(node.left.value,node.right.value)
        else:
            self.scopeChain[-1][node.left.value].usageCount+=1
        for child in node:
            self.visit(child)
            
    def visit_VarDecl(self, node):
        if node.identifier.value not in self.scopeChain[-1]:
            self.scopeChain[-1][node.identifier.value] = varObject(node.identifier.value,'',1)
        else:
            self.scopeChain[-1].get(node.identifier.value).isDefined = 1
        for child in node:
            self.visit(child)
            
    def visit_FuncExpr(self,node):
        self.scopeChain.append(dict())
        for i in node.parameters:
            #self.scopeChain[-1].append(i.value)
            if i.value not in self.scopeChain[-1]:
                self.scopeChain[-1][i.value] = varObject(i.value,'',1)
            else:
                self.scopeChain[-1][i.value].usageCount+=1
        for child in node:
            self.visit(child)
        self.checkForLeaks()
        self.printScope(self.scopeChain.pop(),node)
            
class MyVisitor(ASTVisitor):
    
    def __init__(self):
        self.usageDict = dict()
    
    def generic_visit(self, node):
        """Visit object literal."""
        #print(node)
        if hasattr(node, 'identifier'):
            if hasattr(node.identifier, '_mangle_candidate'):
                if node.identifier._mangle_candidate == True:
                    if self.usageDict.has_key(node.identifier.value):
                        print(node.identifier.value,'bug')
                        self.usageDict[node.identifier.value].append(node)
                    else:
                        self.usageDict[node.identifier.value] = [node]
        if hasattr(node, 'value'):
            if self.usageDict.has_key(node.value):
                self.usageDict[node.value].append(node)
        for child in node:
            self.generic_visit(child)

def removeUnusedVars(tree):
    sym_table = SymbolTable()
    visitor = ScopeTreeVisitor(sym_table)
    visitor.visit(tree)

    fill_scope_references(tree)
    
    mangler = UnusedVariablesVisitor()
    mangler.visit(tree,tree)
    mangler.visit(tree,tree)
    mangler.visit(tree,tree)
    mangler.visit(tree,tree)
    mangler.visit(tree,tree)

inFile = open('angler','r')
outFile = open('deobfuscated','w')
text = inFile.read()
try:
    opts = jsbeautifier.default_options()
    opts.unescape_strings = 1
    text = jsbeautifier.beautify(text,opts)
except:
    pass

#text = cleanLeadingZeros(text)
#x = minify(text, mangle=True, mangle_toplevel=True)
parser = Parser()
tree = parser.parse(text)
#visitor = MyVisitor()
#visitor.generic_visit(tree)
removeUnusedVars(tree)
#testvisitor = TestVisitor()
#testvisitor.visit(tree)
'''sym_table = SymbolTable()
visitor = ScopeTreeVisitor(sym_table)
visitor.visit(tree)
print(visitor.sym_table.globals.symbols)'''

concatvisitor = ConcatVisitor()
concatvisitor.do(tree)
text = minify(tree.to_ecma(), mangle=True, mangle_toplevel=True)
#text = ECMAMinifier().visit(tree)
#text = tree.to_ecma()
opts = jsbeautifier.default_options()
opts.unescape_strings = 1
res = jsbeautifier.beautify(text,opts)
outFile.write(res)
print(res)