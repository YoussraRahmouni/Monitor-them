import pylint.lint
import pylint.reporters.text as text
import io
import os
import sys
pylint_opts = ['--disable=trailing-whitespace', str(sys.argv)]
pylint.lint.Run(pylint_opts)
#os.stat("report.out").st_size == 0
