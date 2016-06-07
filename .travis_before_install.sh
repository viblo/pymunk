#!/bin/bash
set -e

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update;
    
    case $TOXENV in 
    py27)
        brew install python;
        ;;
    py3)
        brew install python3;
        ;;
    esac
    
    PATH=/usr/local/bin:$PATH;
fi; 
