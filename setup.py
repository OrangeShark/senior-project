
from setuptools import setup

setup(name='cn',
    version='0.1',
    author='Erik Edrosa & Leo Shao',
    scripts=['src/src.py'],
    install_requires=['ply'],
    entry_points = {
      'console_scripts': [
        'cn = src:main'
        ],
      }
    )
