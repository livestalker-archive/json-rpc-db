from setuptools import setup, find_packages
from jsonrpcdb import version, PROJECT
from codecs import open
from os import path

root_project = path.abspath(path.dirname(__file__))

with open(path.join(root_project, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PROJECT,
    version=version,

    description='DB API v2.0 for JSON-RPC',
    long_description=long_description,

    url='https://github.com/LiveStalker/json-rpc-db',

    author='Alexey V. Grebenshchikov',
    author_email='mi.aleksio@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',

        'Intended Audience :: Developers',

        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'

        'License :: OSI Approved :: MIT License',
    ],

    keywords='db-api json-rpc',

    packages=find_packages(exclude=['tests*']),

    install_requires=['requests'],

    extras_require={
        'test': ['coverage', 'json-rpc', 'werkzeug']
    }
)
