import ast
import collections
import sys

StandardModules = {
    "argparse":         (3, 2),
    "importlib":        (3, 1),
    "tkinter.ttk":      (3, 1),
}

Functions = {
    "bytearray.maketrans":                      (3, 1),
    "bytes.maketrans":                          (3, 1),
    "collections.Counter":                      (3, 1),
    "collections.OrderedDict":                  (3, 1),
    "email.generator.BytesGenerator":           (3, 2),
    "email.message_from_binary_file":           (3, 2),
    "email.message_from_bytes":                 (3, 2),
    "functools.lru_cache":                      (3, 2),
    "gzip.compress":                            (3, 2),
    "gzip.decompress":                          (3, 2),
    "itertools.combinations_with_replacement":  (3, 1),
    "itertools.compress":                       (3, 1),
    "logging.config.dictConfig":                (3, 2),
    "logging.NullHandler":                      (3, 1),
    "os.environb":                              (3, 2),
    "os.fsdecode":                              (3, 2),
    "os.fsencode":                              (3, 2),
    "os.getenvb":                               (3, 2),
    "ssl.match_hostname":                       (3, 2),
    "ssl.SSLContext":                           (3, 2),
}

def uniq(a):
    if len(a) == 0:
        return []
    else:
        return [a[0]] + uniq([x for x in a if x != a[0]])

class NodeChecker(ast.NodeVisitor):
    def __init__(self):
        self.vers = collections.defaultdict(list)
        self.vers[(3,0)].append(None)
    def visit_Call(self, node):
        def rollup(n):
            if isinstance(n, ast.Name):
                return n.id
            elif isinstance(n, ast.Attribute):
                r = rollup(n.value)
                if r:
                    return r + "." + n.attr
        name = rollup(node.func)
        if name:
            v = Functions.get(name)
            if v is not None:
                self.vers[v].append(name)
        self.generic_visit(node)
    def visit_Import(self, node):
        for n in node.names:
            v = StandardModules.get(n.name)
            if v is not None:
                self.vers[v].append(n.name)
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        v = StandardModules.get(node.module)
        if v is not None:
            self.vers[v].append(node.module)
        for n in node.names:
            name = node.module + "." + n.name
            v = Functions.get(name)
            if v is not None:
                self.vers[v].append(name)

def get_versions(source):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 3.1 is (3,1)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = ast.parse(source)
    checker = NodeChecker()
    checker.visit(tree)
    return checker.vers

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print("hello world")')
    (3, 0)
    >>> qver("import importlib")
    (3, 1)
    >>> qver("from importlib import x")
    (3, 1)
    >>> qver("import tkinter.ttk")
    (3, 1)
    >>> qver("from collections import Counter")
    (3, 1)
    >>> qver("collections.OrderedDict()")
    (3, 1)
    >>> qver("import functools\\n@functools.lru_cache()\\ndef f(x): x*x")
    (3, 2)
    """
    return max(get_versions(source).keys())

Verbose = False
MinVersion = (3, 0)

files = []
i = 1
while i < len(sys.argv):
    a = sys.argv[i]
    if a == "--test":
        import doctest
        doctest.testmod()
        sys.exit(0)
    if a == "-v" or a == "--verbose":
        Verbose = True
    elif a == "-m" or a == "--min-version":
        i += 1
        MinVersion = tuple(map(int, sys.argv[i].split(".")))
    else:
        files.append(a)
    i += 1

if not files:
    print("""Usage: {0} [options] source ...

    Report minimum Python version required to run given source files.

    -m x.y or --min-version x.y (default 3.0)
        report version triggers at or above version x.y in verbose mode
    -v or --verbose
        print more detailed report of version triggers for each version
""".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

for fn in files:
    try:
        f = open(fn)
        source = f.read()
        f.close()
        ver = get_versions(source)
        if Verbose:
            print(fn)
            for v in sorted([k for k in ver.keys() if k >= MinVersion], reverse=True):
                reasons = [x for x in uniq(ver[v]) if x]
                if reasons:
                    print("\t{0}\t{1}".format(".".join(map(str, v)), ", ".join(reasons)))
        else:
            print("{0}\t{1}".format(".".join(map(str, max(ver.keys()))), fn))
    except SyntaxError as x:
        pass
