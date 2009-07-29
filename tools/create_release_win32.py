import sys, re
import os


def main():
    
    os.chdir("..")
    os.system("python setup.py sdist")
    os.system("python setup.py bdist --formats=msi")
    os.system("python25 setup.py bdist --formats=msi")
    os.system("python setup.py bdist --formats=wininst")
    print("""
    Remember (before running this script!): 
    - change version number in readme, setup.py and __init__ 
    - regenerate the api
    - branch in svn""")
    



if __name__ == "__main__":
    sys.exit(main())



