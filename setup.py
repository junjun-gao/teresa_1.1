# setup.py
from setuptools import setup

setup(
    name='teresa',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        cli=cli:cli
    ''',
)
