from distutils.core import setup
setup(name='btcspendfrom',
      version='1.0',
      description='Command-line utility for scarycoin "coin control"',
      author='Gavin Andresen',
      author_email='gavin@scarycoinfoundation.org',
      requires=['jsonrpc'],
      scripts=['spendfrom.py'],
      )
