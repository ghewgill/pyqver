# pyqver - query required Python version

Greg Hewgill  
[http://hewgill.com](http://hewgill.com)

## INTRODUCTION

This script attempts to identify the minimum version of Python that is required
to execute a particular source file.

When developing Python scripts for distribution, it is desirable to identify
which minimum version of the Python interpreter is required. `pyqver` attempts to
answer this question using a simplistic analysis of the output of the Python
compiler.

When run without the `-v` argument, sources are listed along with the minimum
version of Python required. When run with the `-v` option, each version is
listed along with the reasons why that version is required. For example, for
the `pyqver2.py` script itself:

    pyqver2.py
            2.3     platform

This means that `pyqver2.py` uses the `platform` module, which is a 2.3
feature.

The `pyqver2.py` script is specific to Python 2.x, and `pyqver3.py` is specific
to Python 3.x.

This script was inspired by the following question on Stack Overflow:
[Tool to determine what lowest version of Python required?][1]

  [1]: http://stackoverflow.com/questions/804538/tool-to-determine-what-lowest-version-of-python-required

## REQUIREMENTS

This script requires at least Python 2.3.

## USAGE

    Usage: pyqver[23].py [options] source ...

        Report minimum Python version required to run given source files.

        -m x.y or --min-version x.y (default M.N)
            report version triggers at or above version x.y in verbose mode
        -l or --lint
            print a lint style report showing each offending line
        -v or --verbose
            print more detailed report of version triggers for each version

`M.N` is the default minimum version depending on whether `pyqver2.py` or
`pyqver3.py` is run.

## BUGS

There are currently a few features which are not detected. For example, the 2.6
syntax

    try:
        # ...
    except Exception as x:
        # ...

is not detected because the output of the `compiler` module is the same for
both the old and the new syntax.

The `TODO` file has a few notes of things to do.
