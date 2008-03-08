import epydoc.cli
import sys

def main():
    sys.argv[1:] = ["--config=epydoc.config"]   
    epydoc.cli.cli()

if __name__ == "__main__":
    sys.exit(main())