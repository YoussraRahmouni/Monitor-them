import pylint.lint
import pylint.reporters.text as text
import io
import os
pylint_opts = ['--disable=trailing-whitespace', 'connexion.py']
pylint_output = io.StringIO() # Custom open stream
with open("report.out", "w") as f:
    reporter = text.TextReporter(f)
    pylint.lint.Run(pylint_opts, reporter=reporter, do_exit=False)
os.stat("report.out").st_size == 0