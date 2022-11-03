import os
import sys


def main():
    os.chdir("..")

    print(
        """
    Remember (before running this script!): 
    - change version number in README.rst, setup.py, CITATION.cff and __init__.py
    - test in at least CPython 3.x and Pypy3
    - validate test results of Github Actions
    - write changelog entry and put in changelog.rst
    - make sure all images are optimized (for example with tinypng.com)
    - generate docs before running sdist
    
    """
    )
    print(
        """
    Once the release is done, remember to:
    - tag code on github with version
    - Download dists from github release and appveyor
    - Upload files on pypi (> python -m twine upload dist/*)
    - Update Pymunk entry on pygame.org
    - Update Pymunk on conda-forge
    - Possibly: Make release announcement at the chipmunk forum
    - Possibly: make release announcement on the pyglet list
    - Possibly: make release announcement on the pygame list
    - Possibly: make release announcement on the python announce list
    - Possibly: make release announcement on the kivy mailing list
    - Possibly: make PR to update pymunk in python-for-android (remember test!)
    """
    )
    os.chdir("tools")


if __name__ == "__main__":
    sys.exit(main())
