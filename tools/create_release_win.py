import sys, re
import os
import shutil


def main():
    os.chdir("..")
    shutil.rmtree("dist")
    os.system("python setup.py sdist")
    os.system("python2 setup.py bdist_wheel")
    os.system("python2-64 setup.py bdist_wheel")
    files = os.listdir("dist")
    for file in files:
        # see
        # https://www.python.org/dev/peps/pep-0427/
        # https://www.python.org/dev/peps/pep-0425/
        # bdist_wheel give overly strict tags 
        parts = file.split("-")
        if len(parts) == 5 and parts[-1][-3:] == "whl":
            parts[2] = "py2.py3"
            parts[3] = "none"
        newfile = "-".join(parts)
        os.rename(os.path.join("dist", file), os.path.join("dist", newfile))
    print("""
    Remember (before running this script!): 
    - change version number in readme, setup.py and __init__ 
    - test in at least cpython 2.7, 3.x and pypy
    - validate test results of travis and appveyor
    - write news entry and put in news.rst
    - regenerate the api docs
    """)
    print("""
    Once the relase is done, remember to:
    - Upload files on pypi
    - Update pymunk entry on pygame.org
    - Make release announcement at the chipmunk forum
    - Possibly: make release announcement on the pyglet list
    - Possibly: make release announcement on the pygame list
    - Possibly: make release announcement on the python announce list
    """)
    os.chdir("tools")
    

if __name__ == "__main__":
    sys.exit(main())
