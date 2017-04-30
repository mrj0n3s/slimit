#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 18.04.2017

@author: Mr. Jones
'''
#pip.exe install https://pypi.python.org/packages/ce/3d/1f9ca69192025046f02a02ffc61bfbac2731aab06325a218370fd93e18df/ply-3.10.tar.gz
#pip install jsbeautifier
import hashlib,base64
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
import jsbeautifier,slimitmodifications
from slimit.cfg import FlowNode
       
slimitModifier = slimitmodifications.SlimitModifications()
inFile = open('E:\Test1','r')
outFile = open('deobfuscated','w')
text = inFile.read()
test = """
BITDM = VRWJDZX(LVQNCUV("25H1BK1CM3AP06R06T02W5CY25B1BD1CG3AI06K06M02P20Q17T03V07Y17A01C06E5CH47J5CL43N", WQBLHEUPS));
"""
hash_= hashlib.sha256()
hash_.update(text)
slimitModifier.updateFileHandleName(base64.b32encode(hash_.hexdigest())[0:20])
try:
    opts = jsbeautifier.default_options()
    opts.unescape_strings = 1
    text = jsbeautifier.beautify(text,opts)
except:
    pass

#x = minify(text, mangle=True, mangle_toplevel=True)
parser = Parser()
tree = parser.parse(text)
#unusedvisitor = UnusedObjectsVisitor()
#unusedvisitor.do(tree)
'''sym_table = SymbolTable()
visitor = ScopeTreeVisitor(sym_table)
visitor.visit(tree)
print(visitor.sym_table.globals.symbols)'''

#foldvisitor = FoldingVisitor()
#foldvisitor.do(tree)

cfgvisitor = CFGVisitor()
x = FlowNode()
cfgvisitor.visit(tree,x)
#y = cfg.ConstantTraversal(x)
#y.traverse()

#foldvisitor = FoldingVisitor()
#foldvisitor.do(tree)
#y = cfg.PrintTraversal(x)
#y.traverse()
#text = minify(tree.to_ecma(), mangle=True, mangle_toplevel=True)
#text = ECMAMinifier().visit(tree)
text = tree.to_ecma(True)

opts = jsbeautifier.default_options()
opts.unescape_strings = 1
res = jsbeautifier.beautify(text,opts)
outFile.write(res)
print(res)