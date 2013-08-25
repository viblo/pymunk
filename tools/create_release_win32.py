import sys, re
import os


def main():
    upload_command = ""
    if len(sys.argv) > 1 and sys.argv[1] == "upload":
        upload_command = " upload"
    os.chdir("..")
    os.system("python setup.py sdist" + upload_command)
    os.system("python setup.py bdist --formats=msi")
    os.system("python25 setup.py bdist --formats=msi")
    os.system("python setup.py bdist --formats=wininst" + upload_command)
    print("""
    Remember (before running this script!): 
    - change version number in readme, setup.py and __init__ 
    - test in at least cpython 2.5, 2.6, 3.x and pypy
    - write news entry and put in news.rst
    - make sure chipmunk.dll does not depend on msvcr90.dll!
      (best way is to compile with python 2.5 instead of 2.6)
    - regenerate the api
    - branch in svn
    - run this script with >python create_release_win32.py upload to upload to 
    pypy""")
    print("""
    Once the relase is done, remember to:
    - Upload files on google code and pypi
    - Update pymunk entry on pygame.org
    - Make release announcement at the chipmunk forum
    - Possibly: make release announcement on the pyglet list
    - Possibly: make release announcement on the pygame list
    """)
    



if __name__ == "__main__":
    sys.exit(main())
