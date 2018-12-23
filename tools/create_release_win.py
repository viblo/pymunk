import sys, re
import os
import shutil


def main():
    os.chdir("..")
    shutil.rmtree("dist", True)
    os.system("python setup.py sdist --formats=zip")
    os.system("python2 setup.py bdist_wheel")
    os.system("python2-64 setup.py bdist_wheel")
    
    print("""
    Remember (before running this script!): 
    - change version number in readme, setup.py and __init__ 
    - test in at least CPython 2.7, 3.x and Pypy
    - validate test results of Travis and Appveyor
    - write news entry and put in news.rst
    - make sure all images are optimized (for example with tinypng.com)
    - regenerate the api docs
    
    """)
    print("""
    Once the release is done, remember to:
    - tag code on github with version
    - Upload files on pypi (> python -m twine upload dist/*)
    - Update Pymunk entry on pygame.org
    - Make release announcement at the chipmunk forum
    - Possibly: make release announcement on the pyglet list
    - Possibly: make release announcement on the pygame list
    - Possibly: make release announcement on the python announce list
    - Possibly: make release announcement on the kivy mailing list
    - Possibly: make PR to update pymunk in python-for-android (remember test!)
    """)
    os.chdir("tools")
    

if __name__ == "__main__":
    sys.exit(main())
