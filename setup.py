import os
import runpy

from setuptools import setup

packages = ["pymunk", "pymunk.tests", "pymunk.examples"]
exclude_package_data = {}
if os.getenv("PYMUNK_BUILD_SLIM"):
    packages = ["pymunk", "pymunk.tests"]
    exclude_package_data = {"pymunk.examples": ["*.*"]}


# Do not import pymunk here: its compiled extension may not exist yet.
PymunkBuildExt = runpy.run_path("pymunk_build_support.py")["PymunkBuildExt"]

setup(
    cmdclass={"build_ext": PymunkBuildExt},
    packages=packages,
    exclude_package_data=exclude_package_data,
    cffi_modules=["pymunk/pymunk_extension_build.py:ffibuilder"],
)
