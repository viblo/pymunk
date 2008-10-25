import epydoc.cli
import sys
import os

def main():
    os.chdir("..")
    sys.argv[1:] = ["--config=tools/epydoc.config"]   
    epydoc.cli.cli()

if __name__ == "__main__":
    sys.exit(main())