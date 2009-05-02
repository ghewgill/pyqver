import collections
import compiler
import sys

StandardModules = {
    "__future__":       (2, 1),
    "abc":              (2, 6),
    "ast":              (2, 6),
    "atexit":           (2, 0),
    "bz2":              (2, 3),
    "cgitb":            (2, 2),
    "collections":      (2, 4),
    "contextlib":       (2, 5),
    "cookielib":        (2, 4),
    "csv":              (2, 3),
    "ctypes":           (2, 5),
    "datetime":         (2, 3),
    "decimal":          (2, 4),
    "difflib":          (2, 1),
    "DocXMLRPCServer":  (2, 3),
    "dummy_thread":     (2, 3),
    "dummy_threading":  (2, 3),
    "email":            (2, 2),
    "fractions":        (2, 6),
    "functools":        (2, 5),
    "future_builtins":  (2, 6),
    "hashlib":          (2, 5),
    "heapq":            (2, 3),
    "hmac":             (2, 2),
    "hotshot":          (2, 2),
    "HTMLParser":       (2, 2),
    "inspect":          (2, 1),
    "io":               (2, 6),
    "itertools":        (2, 3),
    "json":             (2, 6),
    "logging":          (2, 3),
    "modulefinder":     (2, 3),
    "msilib":           (2, 5),
    "multiprocessing":  (2, 6),
    "netrc":            (1, 5, 2),
    "numbers":          (2, 6),
    "optparse":         (2, 3),
    "ossaudiodev":      (2, 3),
    "pickletools":      (2, 3),
    "pkgutil":          (2, 3),
    "platform":         (2, 3),
    "pydoc":            (2, 1),
    "runpy":            (2, 5),
    "sets":             (2, 3),
    "shlex":            (1, 5, 2),
    "SimpleXMLRPCServer": (2, 2),
    "spwd":             (2, 5),
    "sqlite3":          (2, 3),
    "ssl":              (2, 6),
    "stringprep":       (2, 3),
    "subprocess":       (2, 4),
    "tarfile":          (2, 3),
    "textwrap":         (2, 3),
    "timeit":           (2, 3),
    "unittest":         (2, 1),
    "uuid":             (2, 5),
    "warnings":         (2, 1),
    "weakref":          (2, 1),
    "winsound":         (1, 5, 2),
    "wsgiref":          (2, 5),
    "xml.dom":          (2, 0),
    "xml.dom.minidom":  (2, 0),
    "xml.dom.pulldom":  (2, 0),
    "xml.etree.ElementTree": (2, 5),
    "xml.parsers.expat":(2, 0),
    "xml.sax":          (2, 0),
    "xml.sax.handler":  (2, 0),
    "xml.sax.saxutils": (2, 0),
    "xml.sax.xmlreader":(2, 0),
    "xmlrpclib":        (2, 2),
    "zipfile":          (1, 6),
    "zipimport":        (2, 3),
    "_ast":             (2, 5),
    "_winreg":          (2, 0),
}

Functions = {
    "enumerate":    (2, 3),
    "frozenset":    (2, 4),
    "set":          (2, 4),
    "sum":          (2, 3),
}

Identifiers = {
    "False":        (2, 2),
    "True":         (2, 2),
}

class NodeChecker(object):
    def __init__(self):
        self.vers = collections.defaultdict(list)
        self.vers[(2,0)].append(None)
    def default(self, node):
        for child in node.getChildNodes():
            self.visit(child)
    def visitCallFunc(self, node):
        if isinstance(node.node, compiler.ast.Name):
            v = Functions.get(node.node.name)
            if v is not None:
                self.vers[v].append(node)
        self.default(node)
    def visitClass(self, node):
        if node.bases:
            self.vers[(2,2)].append(node)
        self.default(node)
    def visitDecorators(self, node):
        self.vers[(2,4)].append(node)
        self.default(node)
    def visitFloorDiv(self, node):
        self.vers[(2,2)].append(node)
        self.default(node)
    def visitGenExpr(self, node):
        self.vers[(2,4)].append(node)
        self.default(node)
    def visitImport(self, node):
        for n in node.names:
            v = StandardModules.get(n[0])
            if v is not None:
                self.vers[v].append(n)
        self.default(node)
    def visitName(self, node):
        v = Identifiers.get(node.name)
        if v is not None:
            self.vers[v].append(node)
        self.default(node)
    def visitYield(self, node):
        self.vers[(2,2)].append(node)
        self.default(node)

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print "hello world"')
    (2, 0)
    >>> qver('class test(object): pass')
    (2, 2)
    >>> qver('yield 1')
    (2, 2)
    >>> qver('a // b')
    (2, 2)
    >>> qver('True')
    (2, 2)
    >>> qver('enumerate(a)')
    (2, 3)
    >>> qver('total = sum')
    (2, 0)
    >>> qver('sum(a)')
    (2, 3)
    >>> qver('(x*x for x in range(5))')
    (2, 4)
    >>> qver('class C:\\n @classmethod\\n def m(): pass')
    (2, 4)
    >>> qver('import hashlib')
    (2, 5)
    >>> qver('import xml.etree.ElementTree')
    (2, 5)
    """
    tree = compiler.parse(source)
    checker = compiler.walk(tree, NodeChecker())
    return max(checker.vers.keys())

if __name__ == "__main__":
    import doctest
    doctest.testmod()
