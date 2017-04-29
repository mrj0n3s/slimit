#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 18.04.2017

@author: Mr. Jones
'''
#pip.exe install https://pypi.python.org/packages/ce/3d/1f9ca69192025046f02a02ffc61bfbac2731aab06325a218370fd93e18df/ply-3.10.tar.gz
#pip install jsbeautifier
from slimit.parser import Parser
from slimit import cfg
from slimit import minify
from slimit.visitors.foldingvisitor import FoldingVisitor
from slimit.visitors.cfgvisitor import CFGVisitor
from slimit.visitors.nodevisitor import ASTVisitor
from slimit.scope import SymbolTable
from slimit.visitors.scopevisitor import (
    ScopeTreeVisitor,
    fill_scope_references,
    mangle_scope_tree,
    UnusedObjectsVisitor,
    )
from slimit.visitors.minvisitor import ECMAMinifier
import jsbeautifier
from slimit.cfg import FlowNode
       
inFile = open('E:\Test1','r')
outFile = open('deobfuscated','w')
text = inFile.read()
text = """
var a, b = 4,
    d = 0;
a = 2 + b + 3;
if (a) {
    d = 1;
} else {
    d = 2;
}
WScript.echo(d);

"""


try:
    opts = jsbeautifier.default_options()
    opts.unescape_strings = 1
    text = jsbeautifier.beautify(text,opts)
except:
    pass

#x = minify(text, mangle=True, mangle_toplevel=True)
parser = Parser()
tree = parser.parse(text)
unusedvisitor = UnusedObjectsVisitor()
unusedvisitor.do(tree)
'''sym_table = SymbolTable()
visitor = ScopeTreeVisitor(sym_table)
visitor.visit(tree)
print(visitor.sym_table.globals.symbols)'''

foldvisitor = FoldingVisitor()
foldvisitor.do(tree)

cfgvisitor = CFGVisitor()
x = FlowNode()
cfgvisitor.visit(tree,x)
y = cfg.ConstantTraversal(x)
y.traverse()

foldvisitor = FoldingVisitor()
foldvisitor.do(tree)
#y = cfg.PrintTraversal(x)
#y.traverse()
#text = minify(tree.to_ecma(), mangle=True, mangle_toplevel=True)
#text = ECMAMinifier().visit(tree)
text = tree.to_ecma()
opts = jsbeautifier.default_options()
opts.unescape_strings = 1
res = jsbeautifier.beautify(text,opts)
outFile.write(res)
print(res)