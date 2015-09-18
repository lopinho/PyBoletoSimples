#!/usr/bin/env python
# coding: utf-8
from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()
    setup(
        name='boletosimples',
        author='Andre Ferreira',
        author_email='lopinho@gmail.com',
        description='Library to use BoletoSimpes.com.br',
        long_description=long_description,
        license='MIT',
        version='0.0.1',
        url='https://github.com/lopinho/PyBoletoSimples',
        packages=['boletosimples'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
