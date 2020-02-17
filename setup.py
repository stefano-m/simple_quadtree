import os.path

from setuptools import setup

MODULE_ROOT = 'src'
MODULE_NAME = 'quadtree'

VERSION = {}
with open(os.path.join(MODULE_ROOT, MODULE_NAME + '.py'), 'rb') as m:
    for line in m:
        if '__version__' in str(line):
            exec(line, VERSION)
            break

try:
    VERSION = VERSION['__version__']
except KeyError:
    raise RuntimeError('Unable to find module version.')

with open('README.rst') as fd:
    LONG_DESCRIPTION = fd.read()

setup(
    name='simple-quadtree',
    description='Pure Python implementation of a simple QuadTree.',
    long_description=LONG_DESCRIPTION,
    author='Stefano Mazzucco',
    author_email='stefano <AT> curso <DOT> re',
    url='https://github.com/stefano-m/simple_quadtree',
    download_url='https://github.com/stefano-m/simple_quadtree/releases',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    package_dir={'': MODULE_ROOT},
    py_modules=[MODULE_NAME],
    version=VERSION,
    zip_safe=True,
)
