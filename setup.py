import info
from setuptools import setup

setup(
    name=info.NAME,
    version=info.VERSION,
    description=info.SHORT_DESCRIPTION,
    long_description=info.LONG_DESCRIPTION,
    url=info.URL,

    author='Daniel Riethmüller',
    license='Apache-2.0',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix'
    ],

    requires=info.DEPENDENCIES
)
