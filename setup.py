import os.path
from setuptools import setup

import pytest_localserver

def read(fname):
    # makes sure that setup can be executed from a different location
    _here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(_here, fname)).read()

setup(
    name='pytest-localserver',
    version = pytest_localserver.VERSION,
    description = 'py.test plugin to test server connections locally.',
    long_description=read('README'),
    license = 'mit',

    author = 'Sebastian Rahlf',
    author_email = 'basti AT redtoad DOT de',

    packages = ['pytest_localserver'],
    install_requires = ['pytest>=2.0.0'],

    # the following makes the plugin available to py.test
    entry_points = {
        'pytest11': [
            'localserver = pytest_localserver.plugin',
        ]
    },

    zip_safe=False,

    classifiers = [
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)