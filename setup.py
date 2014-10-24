import sys
import os
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from setuptools.command.install import install

class post_install(install):
    def run(self):
        #os.system("pip install arches -i https://testpypi.python.org/pypi")        
        
        if sys.platform == 'win32':
            python_exe = os.path.join(sys.prefix, 'Scripts', 'python')
        else:
            python_exe = os.path.join(sys.prefix, 'bin', 'python')
        print '%s manage.py packages --operation setup' % (python_exe)
        os.system('%s manage.py packages --operation setup' % (python_exe))  
        # from arches.setup import get_version
        # get_version(path_to_file=os.path.join(os.path.dirname(__file__), 'hip'))
        install.run(self)

setup(
    name='hip',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='1.0.0',

    description='The Heritage Information Package (HIP)',
    long_description=open('README.txt').read(),
    url='http://archesproject.org/',
    author='Farallon Geographics, Inc',
    author_email='dev@fargeo.com',
    license='GNU AGPL',

    cmdclass={'install': post_install},

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='django arches cultural heritage',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    include_package_data = True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'hip=hip.cli:main',
        ],
    },

    #setup_requires=["hgtools"],

    zip_safe=True,
)