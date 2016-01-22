#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "giantapi",
    version = "1.0",
    packages = find_packages(),
    scripts = ['giantapi.py', 'netwas.py'],
    install_requires = ['requests'],
    author_email = "amr4@princeton.edu",
    description = "NetWAS analysis using GIANT API from Python",
    url = "http://giant-api.princeton.edu",
    zip_safe=False,
)
