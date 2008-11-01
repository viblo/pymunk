import sys, re
import os


def main():
    
    os.chdir("..")
    os.system("python setup.py sdist")
    os.system("python setup.py bdist --formats=wininst")
    print("""remember to (before running this script!): 
    - change version number in readme and __init__ 
    - regenerate the api
    - branch in svn""")
    



if __name__ == "__main__":
    sys.exit(main())



