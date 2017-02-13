from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='digiduck',
    version='1.3.1.b2',
    description='A program to compile Ducky Script to Digispark code',
    long_description=long_description,
    url='https://github.com/uslurper/digiduck',
    author='Uslurper',
    author_email='aklo101256@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='digispark duckyscript pentesting',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['iterutils'],
    entry_points={
        'console_scripts': [
            'digiduck=digiduck:main',
        ],
    },
)
