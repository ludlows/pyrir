# 2019-12
# github.com/ludlows
# Lite Python Package for Room Impulse Response
import numpy
from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import build_ext,cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

extensions = [
    Extension(
        "pyrir.cyrir.cyrir",
        ["pyrir/cyrir/cyrir.pyx"],
        include_dirs=[numpy.get_include()],
        language="c")
]
setup(
    name="pyrir",
    version="0.0.1",
    author="ludlows",
    description="Lite Package for Room Impulse Response",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludlows/pyrir",
    packages=find_packages(),
    package_data={'pyrir':["cyrir/cyrir.pyx", "cyrir/rir.c"]},
    cmdclass = {'build_ext': build_ext},
    ext_modules=cythonize(extensions),
    setup_requires=['numpy', 'scipy', 'cython'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)