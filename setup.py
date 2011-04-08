from setuptools import setup

import pytest_localserver

def read(fname):
    # makes sure that setup can be executed from a different location
    import os.path
    _here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(_here, fname)).read()

setup(
    name='pytest-localserver',
    version = pytest_localserver.VERSION,
    author = 'Sebastian Rahlf',
    author_email = 'basti AT redtoad DOT de',
    license = 'MIT License',
    description = 'py.test plugin to test server connections locally.',
    long_description=read('README'),
    url='http://bitbucket.org/basti/pytest-localserver/',
    download_url='http://bitbucket.org/basti/pytest-localserver/downloads/',

    packages = ['pytest_localserver'],
    install_requires = ['pytest>=2.0.0'],
    entry_points = {'pytest11': ['localserver = pytest_localserver.plugin']},
    zip_safe=False,

    keywords='py.test pytest server localhost http smtp',
    classifiers = [
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing'
    ]
)
