import pylint.lint
import pylint.reporters.text as text
import io
import os
import sys
for file in sys.argv[1:]:
    print(file)
    #pylint_opts = ['--disable=trailing-whitespace', file]
    pylint_opts = ['--rcfile=pylintrc', file]
    pylint.lint.Run(pylint_opts)
