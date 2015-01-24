#!/bin/env python

execfile("interpol/version.py")

from setuptools import setup

setup(
        name="interpol", 
        version=__version__, 
        description="A way to interpolate data yielded from iterators", 
        url="https://github.com/radium226/interpol", 
        license="GPL", 
        packages=["interpol"], 
        zip_safe=True
    )

