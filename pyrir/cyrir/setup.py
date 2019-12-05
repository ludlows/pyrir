import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize, build_ext

extensions = [
    Extension(
        "cyrir",
        ["cyrir.pyx"],
        include_dirs=[numpy.get_include()],
        language="c")
]
setup(
    name="RIR (Room Impulse Response) Python Wrapper",
    cmdclass = {'build_ext': build_ext},
    ext_modules=cythonize(extensions)
)