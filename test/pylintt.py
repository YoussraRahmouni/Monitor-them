import pylint.lint
import pylint.reporters.text as text
import io
import os
import sys
for file in sys.argv:
    print(file)
    pylint_opts = ['--disable=trailing-whitespace', file]
    pylint.lint.Run(pylint_opts)
