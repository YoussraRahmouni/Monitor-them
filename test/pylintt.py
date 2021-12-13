import pylint.lint
import pylint.reporters.text as text
import io
import os
pylint_opts = ['--disable=trailing-whitespace', 'script1.py']
pylint.lint.Run(pylint_opts)
#os.stat("report.out").st_size == 0
