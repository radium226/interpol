#!/bin/env python

from setuptools import setup

setup(
        name="interpol", 
        version="0.1", 
        description="A way to interpolate data yielded from iterators", 
        url="https://github.com/radium226/interpol", 
        license="GPL", 
        packages=["interpol"], 
        zip_safe=True, 
        install_requires=[
            "scipy"
        ]
    )

