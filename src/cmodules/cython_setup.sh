#!/bin/bash  
inst="from setuptools import setup
from Cython.Build import cythonize
setup(
    name='Hello world app',
    ext_modules=cythonize('$1', language_level="3"),
    zip_safe=False,
)"
echo -e "$inst" > setup.py
python setup.py build_ext --inplace
