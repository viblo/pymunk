import os
import sys


def main():
    os.chdir("..")

    print(
        """
    Remember (before running this script!): 
    - change version number in README.rst, setup.py, CITATION.cff and _version.py
    - test in at least CPython 3.x and Pypy3
    - validate test results of Github Actions
    - write changelog entry and put in changelog.rst
    - make sure all images are optimized (for example with tinypng.com)
    - generate docs before running sdist
    - Make sure cffi extensions included in wheel and zip!!!!
    """
    )

    print(
        """
    > python setup.py sdist 
        
    """
    )

    print(
        """
    Once the release is done, remember to:
    - tag code on github with version
    - Download dists from github release
    - Upload files on pypi (> python -m twine upload dist/6.5.0*) with correct verison
    - (not needed anymore) Update Pymunk entry on pygame.org
    - (pr will be craeted automatically when condra forge notice the new version) Update Pymunk on conda-forge
    - Trigger docs build in readthedocs for www.pymunk.org
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
