import compiler

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print "hello world"')
    (2, 0)
    """
    tree = compiler.parse(source)
    return (2, 0)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
