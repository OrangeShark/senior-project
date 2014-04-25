
from setuptools import setup, find_packages

setup(name = 'cnc',
    description = 'A compiler for the C natural programming language',
    url = 'https://github.com/OrangeShark/senior-project',
    license = 'GPL',
    version = '0.1',
    author = 'Erik Edrosa & Leo Shao',
    author_email = 'eedro001@fiu.edu, lshao002@fiu.edu',
    packages = find_packages(),
    scripts = ['cnc.py'],
    install_requires = ['ply'],
    entry_points = {
      'console_scripts': [
        'cnc = cnc:main'
        ],
      }
    )
