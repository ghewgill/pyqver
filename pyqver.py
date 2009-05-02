import collections
import compiler

StandardModules = {
    "hashlib": (2, 5),
}

class NodeChecker(object):
    def __init__(self):
        self.vers = collections.defaultdict(list)
        self.vers[(2,0)].append(None)
    def visitGenExpr(self, node):
        self.vers[(2,4)].append(node)
    def visitImport(self, node):
        for n in node.names:
            v = StandardModules.get(n[0])
            if v is not None:
                self.vers[v].append(n)

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print "hello world"')
    (2, 0)
    >>> qver('import hashlib')
    (2, 5)
    >>> qver('print ",".join(x*x for x in range(5))')
    (2, 4)
    """
    tree = compiler.parse(source)
    checker = NodeChecker()
    compiler.walk(tree, checker)
    return max(checker.vers.keys())

if __name__ == "__main__":
    import doctest
    doctest.testmod()
