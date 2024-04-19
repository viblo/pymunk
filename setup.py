import os

from setuptools import setup  # type: ignore

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Games/Entertainment",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: pygame",
    "Topic :: Scientific/Engineering :: Physics",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]

with open("README.rst") as f:
    long_description = f.read()

packages = ["pymunk", "pymunk.tests", "pymunk.examples"]
exclude_package_data = {}
if os.getenv("PYMUNK_BUILD_SLIM"):
    packages = ["pymunk", "pymunk.tests"]
    exclude_package_data = {"pymunk.examples": ["*.*"]}

setup(
    name="pymunk",
    url="http://www.pymunk.org",
    author="Victor Blomqvist",
    author_email="vb@viblo.se",
    version="6.6.0",  # remember to change me for new versions!
    description="Pymunk is a easy-to-use pythonic 2D physics library",
    long_description=long_description,
    packages=packages,
    # include_package_data=True,
    package_data={"pymunk.examples": ["*.png", "*.wav"]},
    exclude_package_data=exclude_package_data,
    license="MIT License",
    classifiers=classifiers,
    python_requires=">=3.7",
    # Require >1.14.0 since that (and older) has problem with returing structs from functions.
    install_requires=["cffi >= 1.15.0"],
    cffi_modules=["pymunk/pymunk_extension_build.py:ffibuilder"],
    extras_require={
        "dev": ["pyglet < 2.0.0", "pygame", "sphinx", "aafigure", "wheel", "matplotlib"]
    },
    test_suite="pymunk.tests",
)
