from setuptools import setup, Command
import sys


VERSION = '0.4.1'


def read(fname):
    # makes sure that setup can be executed from a different location
    import os.path
    _here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(_here, fname)).read()

# make sure that versions match before uploading anything to the cheeseshop
if 'upload' in sys.argv or 'register' in sys.argv:
    import pytest_localserver
    assert pytest_localserver.VERSION == VERSION


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='pytest-localserver',
    version=VERSION,
    author='Sebastian Rahlf',
    author_email='basti@redtoad.de',
    license='MIT License',
    description='py.test plugin to test server connections locally.',
    long_description=read('README'),
    url='http://bitbucket.org/pytest-dev/pytest-localserver/',
    download_url='http://bitbucket.org/pytest-dev/pytest-localserver/downloads/',

    packages=['pytest_localserver'],
    install_requires=[
        'werkzeug>=0.10'
    ],
    cmdclass={'test': PyTest},
    tests_require=[
        'pytest>=2.0.0',
        'six',
        'requests'
    ],
    entry_points={
        'pytest11': ['localserver = pytest_localserver.plugin']
    },

    zip_safe=False,
    include_package_data=True,

    keywords='py.test pytest server localhost http smtp',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing'
    ]
)
