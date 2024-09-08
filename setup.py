import os

from setuptools import setup  # type: ignore

packages = ["pymunk", "pymunk.tests", "pymunk.examples"]
exclude_package_data = {}
if os.getenv("PYMUNK_BUILD_SLIM"):
    packages = ["pymunk", "pymunk.tests"]
    exclude_package_data = {"pymunk.examples": ["*.*"]}


setup(
    packages=packages,
    exclude_package_data=exclude_package_data,
    cffi_modules=["pymunk/pymunk_extension_build.py:ffibuilder"],
)
