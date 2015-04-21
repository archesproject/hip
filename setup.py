import sys
import os
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding

# Dynamically calculate the version based on arches.VERSION.
version = __import__('arches_hip').__version__

setup(
    name='arches_hip',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    description='The Heritage Information Package (HIP)',
    long_description=open('README.txt').read(),
    url='http://archesproject.org/',
    author='Farallon Geographics, Inc',
    author_email='dev@fargeo.com',
    license='GNU AGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='django arches hip cultural heritage',

    install_requires=[
       'arches>=3.0'
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    include_package_data = True,
    zip_safe=False,
)